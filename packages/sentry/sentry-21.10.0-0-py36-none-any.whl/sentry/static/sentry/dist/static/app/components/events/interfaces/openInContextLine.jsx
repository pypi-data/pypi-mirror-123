Object.defineProperty(exports, "__esModule", { value: true });
exports.OpenInName = exports.OpenInLink = exports.OpenInContainer = exports.OpenInContextLine = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const sentryAppIcon_1 = require("app/components/sentryAppIcon");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const queryString_1 = require("app/utils/queryString");
const recordSentryAppInteraction_1 = require("app/utils/recordSentryAppInteraction");
const OpenInContextLine = ({ lineNo, filename, components }) => {
    const handleRecordInteraction = (slug) => () => {
        (0, recordSentryAppInteraction_1.recordInteraction)(slug, 'sentry_app_component_interacted', {
            componentType: 'stacktrace-link',
        });
    };
    const getUrl = (url) => {
        return (0, queryString_1.addQueryParamsToExistingUrl)(url, { lineNo, filename });
    };
    return (<exports.OpenInContainer columnQuantity={components.length + 1}>
      <div>{(0, locale_1.t)('Open this line in')}</div>
      {components.map(component => {
            const url = getUrl(component.schema.url);
            const { slug } = component.sentryApp;
            const onClickRecordInteraction = handleRecordInteraction(slug);
            return (<exports.OpenInLink key={component.uuid} data-test-id={`stacktrace-link-${slug}`} href={url} onClick={onClickRecordInteraction} onContextMenu={onClickRecordInteraction} openInNewTab>
            <sentryAppIcon_1.SentryAppIcon slug={slug}/>
            <exports.OpenInName>{(0, locale_1.t)(`${component.sentryApp.name}`)}</exports.OpenInName>
          </exports.OpenInLink>);
        })}
    </exports.OpenInContainer>);
};
exports.OpenInContextLine = OpenInContextLine;
exports.OpenInContainer = (0, styled_1.default)('div') `
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(${p => p.columnQuantity}, max-content);
  grid-gap: ${(0, space_1.default)(1)};
  color: ${p => p.theme.subText};
  background-color: ${p => p.theme.background};
  font-family: ${p => p.theme.text.family};
  border-bottom: 1px solid ${p => p.theme.border};
  padding: ${(0, space_1.default)(0.25)} ${(0, space_1.default)(3)};
  box-shadow: ${p => p.theme.dropShadowLightest};
  text-indent: initial;
  overflow: auto;
  white-space: nowrap;
`;
exports.OpenInLink = (0, styled_1.default)(externalLink_1.default) `
  display: inline-grid;
  align-items: center;
  grid-template-columns: max-content auto;
  grid-gap: ${(0, space_1.default)(0.75)};
  color: ${p => p.theme.gray300};
`;
exports.OpenInName = (0, styled_1.default)('strong') `
  color: ${p => p.theme.subText};
  font-weight: 700;
`;
//# sourceMappingURL=openInContextLine.jsx.map