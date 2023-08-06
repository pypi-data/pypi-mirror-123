Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const clippedBox_1 = (0, tslib_1.__importDefault)(require("app/components/clippedBox"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const richHttpContentClippedBoxBodySection_1 = (0, tslib_1.__importDefault)(require("./richHttpContentClippedBoxBodySection"));
const richHttpContentClippedBoxKeyValueList_1 = (0, tslib_1.__importDefault)(require("./richHttpContentClippedBoxKeyValueList"));
const RichHttpContent = ({ data }) => (<react_1.Fragment>
    {(0, utils_1.defined)(data.query) && (<richHttpContentClippedBoxKeyValueList_1.default title={(0, locale_1.t)('Query String')} data={data.query} meta={(0, metaProxy_1.getMeta)(data, 'query')} isContextData/>)}
    {(0, utils_1.defined)(data.fragment) && (<clippedBox_1.default title={(0, locale_1.t)('Fragment')}>
        <errorBoundary_1.default mini>
          <pre>{data.fragment}</pre>
        </errorBoundary_1.default>
      </clippedBox_1.default>)}
    {(0, utils_1.defined)(data.data) && (<richHttpContentClippedBoxBodySection_1.default data={data.data} meta={(0, metaProxy_1.getMeta)(data, 'data')} inferredContentType={data.inferredContentType}/>)}
    {(0, utils_1.defined)(data.cookies) && Object.keys(data.cookies).length > 0 && (<richHttpContentClippedBoxKeyValueList_1.default defaultCollapsed title={(0, locale_1.t)('Cookies')} data={data.cookies} meta={(0, metaProxy_1.getMeta)(data, 'cookies')}/>)}
    {(0, utils_1.defined)(data.headers) && (<richHttpContentClippedBoxKeyValueList_1.default title={(0, locale_1.t)('Headers')} data={data.headers} meta={(0, metaProxy_1.getMeta)(data, 'headers')}/>)}
    {(0, utils_1.defined)(data.env) && (<richHttpContentClippedBoxKeyValueList_1.default defaultCollapsed title={(0, locale_1.t)('Environment')} data={data.env} meta={(0, metaProxy_1.getMeta)(data, 'env')}/>)}
  </react_1.Fragment>);
exports.default = RichHttpContent;
//# sourceMappingURL=richHttpContent.jsx.map