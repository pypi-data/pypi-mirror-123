Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const abstractIntegrationDetailedView_1 = (0, tslib_1.__importDefault)(require("./abstractIntegrationDetailedView"));
const constants_1 = require("./constants");
class SentryAppDetailedView extends abstractIntegrationDetailedView_1.default {
    constructor() {
        super(...arguments);
        this.tabs = ['overview'];
        this.trackClick = () => {
            this.trackIntegrationAnalytics('integrations.installation_start');
        };
    }
    get integrationType() {
        return 'document';
    }
    get integration() {
        const { integrationSlug } = this.props.params;
        const documentIntegration = constants_1.documentIntegrations[integrationSlug];
        if (!documentIntegration) {
            throw new Error(`No document integration of slug ${integrationSlug} exists`);
        }
        return documentIntegration;
    }
    get description() {
        return this.integration.description;
    }
    get author() {
        return this.integration.author;
    }
    get resourceLinks() {
        return this.integration.resourceLinks;
    }
    get installationStatus() {
        return null;
    }
    get integrationName() {
        return this.integration.name;
    }
    get featureData() {
        return this.integration.features;
    }
    componentDidMount() {
        super.componentDidMount();
        this.trackIntegrationAnalytics('integrations.integration_viewed', {
            integration_tab: 'overview',
        });
    }
    renderTopButton() {
        return (<externalLink_1.default href={this.integration.docUrl} onClick={this.trackClick}>
        <LearnMoreButton size="small" priority="primary" style={{ marginLeft: (0, space_1.default)(1) }} data-test-id="learn-more" icon={<StyledIconOpen size="xs"/>}>
          {(0, locale_1.t)('Learn More')}
        </LearnMoreButton>
      </externalLink_1.default>);
    }
    // No configurations.
    renderConfigurations() {
        return null;
    }
}
const LearnMoreButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const StyledIconOpen = (0, styled_1.default)(icons_1.IconOpen) `
  transition: 0.1s linear color;
  margin: 0 ${(0, space_1.default)(0.5)};
  position: relative;
  top: 1px;
`;
exports.default = (0, withOrganization_1.default)(SentryAppDetailedView);
//# sourceMappingURL=docIntegrationDetailedView.jsx.map