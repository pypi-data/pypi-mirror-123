Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function getSdkUpdateSuggestion({ sdk, suggestion, shortStyle = false, capitalized = false, }) {
    function getUpdateSdkContent({ newSdkVersion, sdkName }) {
        if (capitalized) {
            return sdk
                ? shortStyle
                    ? (0, locale_1.tct)('Update to [sdk-name]@v[new-sdk-version]', {
                        'sdk-name': sdkName,
                        'new-sdk-version': newSdkVersion,
                    })
                    : (0, locale_1.tct)('Update your SDK from [sdk-name]@v[sdk-version] to [sdk-name]@v[new-sdk-version]', {
                        'sdk-name': sdkName,
                        'sdk-version': sdk.version,
                        'new-sdk-version': newSdkVersion,
                    })
                : (0, locale_1.t)('Update your SDK version');
        }
        return sdk
            ? shortStyle
                ? (0, locale_1.tct)('update to [sdk-name]@v[new-sdk-version]', {
                    'sdk-name': sdkName,
                    'new-sdk-version': newSdkVersion,
                })
                : (0, locale_1.tct)('update your SDK from [sdk-name]@v[sdk-version] to [sdk-name]@v[new-sdk-version]', {
                    'sdk-name': sdkName,
                    'sdk-version': sdk.version,
                    'new-sdk-version': newSdkVersion,
                })
            : (0, locale_1.t)('update your SDK version');
    }
    const getTitleData = () => {
        switch (suggestion.type) {
            case 'updateSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: getUpdateSdkContent(suggestion),
                };
            case 'changeSdk':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.sdkUrl,
                    content: capitalized
                        ? (0, locale_1.tct)('Migrate to [recommended-sdk-version]', {
                            'recommended-sdk-version': suggestion.newSdkName,
                        })
                        : (0, locale_1.tct)('migrate to [recommended-sdk-version]', {
                            'recommended-sdk-version': suggestion.newSdkName,
                        }),
                };
            case 'enableIntegration':
                return {
                    href: suggestion === null || suggestion === void 0 ? void 0 : suggestion.integrationUrl,
                    content: capitalized
                        ? (0, locale_1.tct)('Enable the [recommended-integration-name]', {
                            'recommended-integration-name': suggestion.integrationName,
                        })
                        : (0, locale_1.tct)('enable the [recommended-integration-name] integration', {
                            'recommended-integration-name': suggestion.integrationName,
                        }),
                };
            default:
                return null;
        }
    };
    const getTitle = () => {
        const titleData = getTitleData();
        if (!titleData) {
            return null;
        }
        const { href, content } = titleData;
        if (!href) {
            return content;
        }
        return <externalLink_1.default href={href}>{content}</externalLink_1.default>;
    };
    const title = <react_1.Fragment>{getTitle()}</react_1.Fragment>;
    if (!suggestion.enables.length) {
        return title;
    }
    const alertContent = suggestion.enables
        .map((subSuggestion, index) => {
        const subSuggestionContent = getSdkUpdateSuggestion({
            suggestion: subSuggestion,
            sdk,
            capitalized,
        });
        if (!subSuggestionContent) {
            return null;
        }
        return <listItem_1.default key={index}>{subSuggestionContent}</listItem_1.default>;
    })
        .filter(content => !!content);
    if (!alertContent.length) {
        return title;
    }
    return (<span>
      {(0, locale_1.tct)('[title] so you can:', { title })}
      <StyledList symbol="bullet">{alertContent}</StyledList>
    </span>);
}
exports.default = getSdkUpdateSuggestion;
const StyledList = (0, styled_1.default)(list_1.default) `
  margin-top: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=getSdkUpdateSuggestion.jsx.map