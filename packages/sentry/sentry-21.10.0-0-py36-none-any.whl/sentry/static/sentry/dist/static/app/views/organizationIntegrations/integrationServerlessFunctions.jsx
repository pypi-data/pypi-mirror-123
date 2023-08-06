Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
// eslint-disable-next-line simple-import-sort/imports
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const panels_1 = require("app/components/panels");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const locale_1 = require("app/locale");
const integrationUtil_1 = require("app/utils/integrationUtil");
const integrationServerlessRow_1 = (0, tslib_1.__importDefault)(require("./integrationServerlessRow"));
class IntegrationServerlessFunctions extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleFunctionUpdate = (serverlessFunctionUpdate, index) => {
            const serverlessFunctions = [...this.serverlessFunctions];
            const serverlessFunction = Object.assign(Object.assign({}, serverlessFunctions[index]), serverlessFunctionUpdate);
            serverlessFunctions[index] = serverlessFunction;
            this.setState({ serverlessFunctions });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { serverlessFunctions: [] });
    }
    getEndpoints() {
        const orgSlug = this.props.organization.slug;
        return [
            [
                'serverlessFunctions',
                `/organizations/${orgSlug}/integrations/${this.props.integration.id}/serverless-functions/`,
            ],
        ];
    }
    get serverlessFunctions() {
        return this.state.serverlessFunctions;
    }
    onLoadAllEndpointsSuccess() {
        (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.serverless_functions_viewed', {
            integration: this.props.integration.provider.key,
            integration_type: 'first_party',
            num_functions: this.serverlessFunctions.length,
            organization: this.props.organization,
        });
    }
    renderBody() {
        return (<react_1.Fragment>
        <alert_1.default type="info">
          {(0, locale_1.t)('Manage your AWS Lambda functions below. Only Node and Python runtimes are currently supported.')}
        </alert_1.default>
        <panels_1.Panel>
          <StyledPanelHeader disablePadding hasButtons>
            <NameHeader>{(0, locale_1.t)('Name')}</NameHeader>
            <LayerStatusWrapper>{(0, locale_1.t)('Layer Status')}</LayerStatusWrapper>
            <EnableHeader>{(0, locale_1.t)('Enabled')}</EnableHeader>
          </StyledPanelHeader>
          <StyledPanelBody>
            {this.serverlessFunctions.map((serverlessFunction, i) => (<integrationServerlessRow_1.default key={serverlessFunction.name} serverlessFunction={serverlessFunction} onUpdateFunction={(update) => this.handleFunctionUpdate(update, i)} {...this.props}/>))}
          </StyledPanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)(IntegrationServerlessFunctions);
const StyledPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  padding: ${(0, space_1.default)(2)};
  display: grid;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  grid-template-columns: 2fr 1fr 0.5fr;
  grid-template-areas: 'function-name layer-status enable-switch';
`;
const HeaderText = (0, styled_1.default)('div') `
  flex: 1;
`;
const StyledPanelBody = (0, styled_1.default)(panels_1.PanelBody) ``;
const NameHeader = (0, styled_1.default)(HeaderText) `
  grid-area: function-name;
`;
const LayerStatusWrapper = (0, styled_1.default)(HeaderText) `
  grid-area: layer-status;
`;
const EnableHeader = (0, styled_1.default)(HeaderText) `
  grid-area: enable-switch;
`;
//# sourceMappingURL=integrationServerlessFunctions.jsx.map