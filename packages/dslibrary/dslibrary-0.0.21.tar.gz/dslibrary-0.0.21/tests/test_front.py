import unittest
import mock
import io
import os
import numpy
import pandas
import shutil
import tempfile

from dslibrary import DSLibrary
from dslibrary.front import EVALUATION_RESULT_ALIAS, METRICS_ALIAS, DSLibraryException
from dslibrary.metadata import Metadata
from dslibrary.transport.to_local import DSLibraryLocal


class TestFront(unittest.TestCase):

    def test_metadata(self):
        """
        The base class doesn't know how to get metadata so it returns a null instance.
        """
        dsl = DSLibrary()
        m = dsl.get_metadata()
        assert isinstance(m, Metadata)
        assert m.uri == ""
        assert m.entry_points == {}

    def test_open_resource__input_mapping(self):
        """
        Options for input come from mapping values, which override supplied values.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append((path, mode, kwargs))
                return "H"
        MyInst(spec={"inputs": {"a": {"uri": "aaa", "option1": 1, "option3": 3}}}).open_resource("a", option1=2, option2=22)
        assert log[0] == ('aaa', 'rb', {'option1': 1, 'option2': 22, 'option3': 3}), log[0]

    def test_open_resource__output_mapping(self):
        """
        Options for output come from mapping values, which override supplied values.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append((path, mode, kwargs))
                return "H"
        MyInst(spec={"outputs": {"a": {"uri": "aaa", "option1": 1, "option3": 3}}}).open_resource("a", 'w', option1=2, option2=22)
        self.assertEqual(log[0], ('aaa', 'w', {'option1': 1, 'option2': 22, 'option3': 3}))

    def test_open_resource__bypass_mapping(self):
        """
        Most inputs and outputs are mapped, but you can bypass mapping and specify a URI to open or a local file.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append((path, mode, kwargs))
                return "H"
        MyInst().open_resource("s3://bucket/path", open_option_1=1)
        assert log[0] == ('s3://bucket/path', 'rb', {'open_option_1': 1})
        MyInst().open_resource("./local/file")
        assert log[1] == ('./local/file', 'rb', {})

    def test_open_model_binary(self):
        """
        The default implementation just assumes certain filenames for the 'model-binary' data.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append((path, mode, kwargs))
                return "H"
        MyInst().open_model_binary()
        assert log[0] == ('model-binary', 'rb', {})
        MyInst().open_model_binary("part1")
        assert log[1] == ('model-binary/part1', 'rb', {})

    def test_set_evaluation_result(self):
        """
        Model evaluation code can use this hook to report whether the model passed or failed.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                buf = io.StringIO()
                buf.close = lambda: None
                log.append((path, buf))
                return buf
        MyInst().set_evaluation_result(True)
        MyInst().set_evaluation_result(False, reason="because")
        assert log[0][0] == log[1][0] == EVALUATION_RESULT_ALIAS
        r = log[0][1].getvalue()
        assert r == '{"uri": "", "success": true}\n', r
        r = log[1][1].getvalue()
        assert r == '{"uri": "", "success": false, "reason": "because"}\n', r

    def test_get_sql_connection__mapping(self):
        """
        The normal use case is have the caller supply all the connection information.
        """
        dsl = DSLibrary(spec={"inputs": {"db": {"uri": "mysql://host/db", "username": "u"}}})
        def connect(user, host, database, **kwargs):
            assert user == "u"
            assert host == "host"
            assert database == "db"
            return "CONN"
        with mock.patch("pymysql.connect", connect):
            r = dsl.get_sql_connection("db")
            assert r == "CONN"

    def test_write_resources__dataframes_and_series(self):
        """
        Several types are supported for columnar data.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                buf = io.StringIO()
                buf.close = lambda: None
                log.append((path, buf))
                return buf
        dsl = MyInst()
        # series
        dsl.write_resource("x", pandas.Series([1, 2, 3]))
        assert log[0][0] == "x"
        self.assertEqual(log[0][1].getvalue(), 'x\n1\n2\n3\n')
        log.clear()
        # numpy array
        dsl.write_resource("x", numpy.array([1, 2, 3]))
        assert log[0][0] == "x"
        self.assertEqual(log[0][1].getvalue(), 'x\n1\n2\n3\n')
        log.clear()
        # dataframe
        dsl.write_resource("x", pandas.DataFrame({"y": [1, 2, 3]}))
        assert log[0][0] == "x"
        self.assertEqual(log[0][1].getvalue(), 'y\n1\n2\n3\n')
        log.clear()

    def test_default_metrics_output(self):
        project = tempfile.mkdtemp()
        dsl = DSLibraryLocal(project)
        dsl.log_metric("x", 1)
        r = dsl.get_last_metric("x")
        assert r.value == 1
        # verify it was written as JSON
        fn = os.path.join(project, METRICS_ALIAS)
        assert os.path.exists(fn)
        with open(fn, 'r') as f_r:
            assert f_r.read().startswith("{")
        shutil.rmtree(project)

    def test_alt_metrics_output1(self):
        project = tempfile.mkdtemp()
        dsl = DSLibraryLocal(project, spec={"outputs": {METRICS_ALIAS: {"format": "csv"}}})
        dsl.log_metric("x", 1)
        # verify it was written as CSV
        fn = os.path.join(project, METRICS_ALIAS)
        assert os.path.exists(fn)
        with open(fn, 'r') as f_r:
            assert f_r.read().startswith("uri,")
        shutil.rmtree(project)

    def test_alt_metrics_output2(self):
        project = tempfile.mkdtemp()
        dsl = DSLibraryLocal(project, spec={"outputs": {METRICS_ALIAS: {"uri": "metrics.csv"}}})
        dsl.log_metric("x", 1)
        # verify it was written as CSV
        fn = os.path.join(project, "metrics.csv")
        assert os.path.exists(fn)
        with open(fn, 'r') as f_r:
            assert f_r.read().startswith("uri,")
        shutil.rmtree(project)

    def test_model_pickling(self):
        project = tempfile.mkdtemp()
        dsl = DSLibraryLocal(project, spec={"outputs": {METRICS_ALIAS: {"uri": "metrics.csv"}}})
        # save and restore
        my_model = {"x": 1}
        dsl.save_pickled_model(my_model)
        restored = dsl.load_pickled_model()
        assert restored == my_model
        # verify local storage
        assert os.path.exists(project + "/model-binary")
        shutil.rmtree(project)

    def test_open_resource__default_uri(self):
        """
        Specify a name and a default URI, for cleaner overriding.
        """
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append((path, kwargs))
                return "H"
        MyInst().open_resource("x", uri="default")
        MyInst(spec={"inputs": {"x": {"uri": "override", "option1": 1}}}).open_resource("x", uri="default")
        self.assertEqual(log, [('default', {}), ('override', {'option1': 1})])

    def test_load_dataframe__default_uri(self):
        log = []
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append(path)
                return io.BytesIO(b"x\n1\n2")
        df = MyInst().load_dataframe("x", uri="default.csv")
        df = MyInst(spec={"inputs": {"x": {"uri": "override.csv"}}}).load_dataframe("x", uri="default.csv")
        self.assertEqual(log[0], 'default.csv')
        self.assertEqual(log[-1], 'override.csv')

    def test_load_dataframe__from_sql(self):
        log = []
        class MyInst(DSLibrary):
            def get_sql_connection(self, resource_name: str, for_write: bool=False, **kwargs):
                class DbCursor(object):
                    description = [("x", None)]
                    def execute(self, sql):
                        log.append(sql)
                    def __iter__(self):
                        return iter([(1,), (2,)])
                class DbConn(object):
                    def cursor(self):
                        return DbCursor()
                    def close(self):
                        log.append("close")
                return DbConn()
        df = MyInst().load_dataframe("x", sql_table="table1")
        self.assertEqual(list(df.x), [1, 2])
        self.assertEqual(log, ['SELECT * from table1', 'close'])

    def test_load_dataframe__from_nosql(self):
        class MyInst(DSLibrary):
            def get_nosql_connection(self, resource_name: str, for_write: bool=False, **kwargs):
                class MyNoSql(object):
                    def query(self, collection, **kwargs):
                        assert collection == "table1"
                        return [{"x": 1}, {"x": 2}]
                return MyNoSql()
        df = MyInst().load_dataframe("x", nosql_collection="table1")
        self.assertEqual(list(df.x), [1, 2])

    def test_load_dataframe__sql__custom_open_args(self):
        """
        Custom arguments can be passed through to get_sql_connection().
        """
        class MyInst(DSLibrary):
            def get_sql_connection(self, resource_name: str, database: str=None, for_write: bool=False, **kwargs):
                assert resource_name == "engine"
                assert database == "db"
                assert kwargs["custom1"] == 123
                class DbCursor(object):
                    description = [("x", None)]
                    def execute(self, sql):
                        pass
                    def __iter__(self):
                        return iter([])
                class DbConn(object):
                    def cursor(self):
                        return DbCursor()
                    def close(self):
                        pass
                return DbConn()
        MyInst().load_dataframe("engine", sql_table="table1", database="db", custom1=123)

    def test_open_resource__named_filesystem(self):
        """
        A resource can be opened through a specified filesystem engine/provider.
        """
        class MyInst(DSLibrary):
            def get_filesystem_connection(self, resource_name: str, for_write: bool=False, **kwargs):
                assert resource_name == "fs"
                assert kwargs.get("custom1") == 111
                class FS(object):
                    def open(self, path, mode):
                        assert path == "path"
                        assert mode == "r"
                        return "FH"
                return FS()
        r = MyInst().open_resource("path", mode="r", filesystem="fs", custom1=111)
        assert r == "FH"

    def test_load_dataframe__named_filesystem(self):
        """
        A dataframe can be opened through a specified filesystem engine/provider.
        """
        class MyInst(DSLibrary):
            def get_filesystem_connection(self, resource_name: str, for_write: bool=False, **kwargs):
                assert resource_name == "fs"
                class FS(object):
                    def open(self, path, mode):
                        assert path == "path"
                        assert mode == "rb"
                        return io.BytesIO(b"x\n1\n2\n3")
                return FS()
        df = MyInst().load_dataframe("path", filesystem="fs", format="csv")
        assert list(df.x) == [1, 2, 3]

    def test_rw_run_data(self):
        writes = {}
        class MyInst(DSLibrary):
            def open_run_data(self, filename: str, mode: str='rb'):
                if mode == 'rb':
                    v = writes[filename].getvalue()
                    return io.BytesIO(v)
                wr = io.BytesIO()
                writes[filename] = wr
                wr.close = lambda: None
                return wr
        dsl = MyInst()
        df = pandas.DataFrame({"x": [1, 2]})
        dsl.write_run_data("x.csv", df)
        self.assertEqual(writes["x.csv"].getvalue(), b'x\n1\n2\n')
        df2 = dsl.load_dataframe("x.csv", run_data=True)
        self.assertEqual(list(df2.x), list(df.x))
        self.assertEqual(dsl.read_run_data("x.csv"), b'x\n1\n2\n')

    def test_open_args_passed_through_to_opener(self):
        log = []
        inst = self
        class MyInst(DSLibrary):
            def _opener(self, path: str, mode: str, **kwargs):
                log.append(path)
                inst.assertEqual(kwargs, {'arg1': 123})
                return io.BytesIO(b"abc")
        # just a filename
        fh = MyInst().open_resource("x", arg1=123, format="xyz")
        assert fh.read() == b"abc"
        # uri overrides name
        fh = MyInst().open_resource("x", uri="default.csv", arg1=123, format="xyz")
        assert fh.read() == b"abc"
        # input mapping maps 'x' to something else
        fh = MyInst(spec={"inputs": {"x": {"uri": "override.csv"}}}).open_resource("x", uri="default.csv", arg1=123, format="xyz")
        assert fh.read() == b"abc"
        # verify filenames
        self.assertEqual(log, ['x', 'default.csv', 'override.csv'])

    def test_setup_code_paths(self):
        """
        You can cause 'sys.path' to be extended to include particular folders.
        This is normally done using an environment variable.  Here we are just testing the method that applies the
        changes.
        """
        inst = DSLibrary()
        inst._spec = {"code_paths": ["a", "b"]}
        mock_paths = []
        with mock.patch("sys.path", mock_paths):
            inst._setup_code_paths()
        self.assertEqual(mock_paths, ["a", "b"])

    def test_abstract_base_methods(self):
        """
        The methods that have to be filled in raise exceptions when called.
        """
        inst = DSLibrary()
        self.assertRaises(DSLibraryException, lambda: inst._opener("path", mode='r'))
        self.assertRaises(DSLibraryException, lambda: inst.open_run_data("fn"))

    def test_get_filesystem_connection(self):
        """
        The default filesystem accessor.
        """
        inst = DSLibrary()
        log = []
        with mock.patch("dslibrary.front.connect_to_filesystem", lambda **k: log.append(k) or "FS"):
            fs = inst.get_filesystem_connection("resource", for_write=True, arg1=123)
            self.assertEqual(fs, "FS")
        self.assertEqual(log, [{'uri': 'resource', 'for_write': True, 'arg1': 123}])

    def test_get_sql_connection(self):
        """
        The default SQL accessor.
        """
        inst = DSLibrary()
        log = []
        with mock.patch("dslibrary.front.connect_to_database", lambda **k: log.append(k) or "NoSqlConn"):
            fs = inst.get_sql_connection("resource", for_write=True, arg1=123)
            self.assertEqual(fs, "NoSqlConn")
        self.assertEqual(log, [{'uri': 'resource', 'library': None, 'for_write': True, 'arg1': 123}])

    def test_get_nosql_connection(self):
        """
        The default NoSQL accessor.
        """
        inst = DSLibrary()
        log = []
        with mock.patch("dslibrary.front.connect_to_nosql", lambda **k: log.append(k) or "SqlConn"):
            fs = inst.get_nosql_connection("resource", for_write=True, arg1=123)
            self.assertEqual(fs, "SqlConn")
        self.assertEqual(log, [{'uri': 'resource', 'library': None, 'for_write': True, 'arg1': 123}])

    def test_log_mlflow(self):
        inst = DSLibrary()
        inst._mlflow_all = True
        log = []
        with mock.patch("mlflow.log_param", lambda k, v: log.append((k, v))):
            inst.log_param("x", 1)
        self.assertEqual(log, [("x", 1)])
        log.clear()
        with mock.patch("mlflow.log_metric", lambda *a: log.append(a)):
            inst.log_metric("q", 222)
            inst.log_metrics({"z": 9}, step=2)
        self.assertEqual(log, [('q', 222, 0), ('z', 9, 2)])
        log.clear()
        with mock.patch("mlflow.log_dict", lambda *a: log.append(a)):
            inst.log_dict({"x": 1}, "f.json")
        self.assertEqual(log, [({'x': 1}, 'f.json')])
        log.clear()
        with mock.patch("mlflow.log_artifact", lambda *a: log.append(a)):
            inst.log_artifact("f_local", "f_store")
        self.assertEqual(log, [('f_local', 'f_store')])
        log.clear()
        # not a log function but close enough
        self.assertRaises(DSLibraryException, lambda: inst.get_metrics("x"))

    def test_mlflow_start_end(self):
        inst = DSLibrary()
        inst._mlflow_all = True
        log = []
        with mock.patch("mlflow.mlflow.start_run", lambda: log.append("start")):
            with mock.patch("mlflow.mlflow.end_run", lambda: log.append("end")):
                with mock.patch("mlflow.active_run", lambda: log.append("active_run")):
                    # TODO mock this: mlflow.active_run().info.run_id
                    with inst.start_run():
                        pass
        self.assertEqual(log, ['start', 'active_run', 'end'])

