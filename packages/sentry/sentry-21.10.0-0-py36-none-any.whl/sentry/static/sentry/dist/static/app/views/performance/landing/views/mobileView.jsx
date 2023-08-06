Object.defineProperty(exports, "__esModule", { value: true });
exports.MobileView = void 0;
const tslib_1 = require("tslib");
const pageError_1 = require("app/utils/performance/contexts/pageError");
const table_1 = (0, tslib_1.__importDefault)(require("../../table"));
const data_1 = require("../data");
function MobileView(props) {
    return (<div>
      <table_1.default {...props} columnTitles={data_1.MOBILE_COLUMN_TITLES} // TODO(k-fish): Add react native column titles
     setError={(0, pageError_1.usePageError)().setPageError}/>
    </div>);
}
exports.MobileView = MobileView;
//# sourceMappingURL=mobileView.jsx.map