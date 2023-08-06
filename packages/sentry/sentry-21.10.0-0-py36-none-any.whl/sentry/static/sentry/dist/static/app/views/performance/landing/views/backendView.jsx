Object.defineProperty(exports, "__esModule", { value: true });
exports.BackendView = void 0;
const tslib_1 = require("tslib");
const pageError_1 = require("app/utils/performance/contexts/pageError");
const table_1 = (0, tslib_1.__importDefault)(require("../../table"));
const data_1 = require("../data");
function BackendView(props) {
    return (<div>
      <table_1.default {...props} columnTitles={data_1.BACKEND_COLUMN_TITLES} setError={(0, pageError_1.usePageError)().setPageError}/>
    </div>);
}
exports.BackendView = BackendView;
//# sourceMappingURL=backendView.jsx.map