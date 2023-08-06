Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const summary_1 = (0, tslib_1.__importDefault)(require("./summary"));
function Http({ breadcrumb, searchTerm, linkedEvent }) {
    const { data } = breadcrumb;
    const renderUrl = (url) => {
        if (typeof url === 'string') {
            const content = <highlight_1.default text={searchTerm}>{url}</highlight_1.default>;
            return url.match(/^https?:\/\//) ? (<externalLink_1.default data-test-id="http-renderer-external-link" href={url}>
          {content}
        </externalLink_1.default>) : (<span>{content}</span>);
        }
        try {
            return <highlight_1.default text={searchTerm}>{JSON.stringify(url)}</highlight_1.default>;
        }
        catch (_a) {
            return (0, locale_1.t)('Invalid URL');
        }
    };
    const statusCode = data === null || data === void 0 ? void 0 : data.status_code;
    return (<summary_1.default kvData={(0, omit_1.default)(data, ['method', 'url', 'status_code'])}>
      {linkedEvent}
      {(data === null || data === void 0 ? void 0 : data.method) && (<annotatedText_1.default value={<strong>
              <highlight_1.default text={searchTerm}>{`${data.method} `}</highlight_1.default>
            </strong>} meta={(0, metaProxy_1.getMeta)(data, 'method')}/>)}
      {(data === null || data === void 0 ? void 0 : data.url) && (<annotatedText_1.default value={renderUrl(data.url)} meta={(0, metaProxy_1.getMeta)(data, 'url')}/>)}
      {(0, utils_1.defined)(statusCode) && (<annotatedText_1.default value={<highlight_1.default data-test-id="http-renderer-status-code" text={searchTerm}>{` [${statusCode}]`}</highlight_1.default>} meta={(0, metaProxy_1.getMeta)(data, 'status_code')}/>)}
    </summary_1.default>);
}
exports.default = Http;
//# sourceMappingURL=http.jsx.map