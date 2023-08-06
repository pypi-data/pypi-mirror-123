Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const utils_1 = require("app/utils");
const summary_1 = (0, tslib_1.__importDefault)(require("./summary"));
function Exception({ breadcrumb, searchTerm, linkedEvent }) {
    const { data, message } = breadcrumb;
    const dataValue = data === null || data === void 0 ? void 0 : data.value;
    return (<summary_1.default kvData={(0, omit_1.default)(data, ['type', 'value'])}>
      {linkedEvent}
      {(data === null || data === void 0 ? void 0 : data.type) && (<annotatedText_1.default value={<strong>
              <highlight_1.default text={searchTerm}>{`${data.type}: `}</highlight_1.default>
            </strong>} meta={(0, metaProxy_1.getMeta)(data, 'type')}/>)}
      {(0, utils_1.defined)(dataValue) && (<annotatedText_1.default value={<highlight_1.default text={searchTerm}>
              {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) ? `${dataValue}. ` : dataValue}
            </highlight_1.default>} meta={(0, metaProxy_1.getMeta)(data, 'value')}/>)}
      {message && (<annotatedText_1.default value={<highlight_1.default text={searchTerm}>{message}</highlight_1.default>} meta={(0, metaProxy_1.getMeta)(breadcrumb, 'message')}/>)}
    </summary_1.default>);
}
exports.default = Exception;
//# sourceMappingURL=exception.jsx.map