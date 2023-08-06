Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const mobx_react_1 = require("mobx-react");
const qs = (0, tslib_1.__importStar)(require("query-string"));
const indicator_1 = require("app/actionCreators/indicator");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
const sentryProjectSelectorField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/sentryProjectSelectorField"));
const footerWithButtons_1 = (0, tslib_1.__importDefault)(require("./components/footerWithButtons"));
const headerWithHelp_1 = (0, tslib_1.__importDefault)(require("./components/headerWithHelp"));
class AwsLambdaProjectSelect extends React.Component {
    constructor() {
        super(...arguments);
        this.model = new model_1.default();
        this.handleSubmit = (e) => {
            e.preventDefault();
            const data = this.model.getData();
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Submitting\u2026'));
            this.model.setFormSaving();
            const { location: { origin }, } = window;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            const newUrl = `${origin}/extensions/aws_lambda/setup/?${qs.stringify(data)}`;
            window.location.assign(newUrl);
        };
    }
    render() {
        const { projects } = this.props;
        // TODO: Add logic if no projects
        return (<React.Fragment>
        <headerWithHelp_1.default docsUrl="https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/"/>
        <StyledList symbol="colored-numeric">
          <React.Fragment />
          <listItem_1.default>
            <h3>{(0, locale_1.t)('Select a project for your AWS Lambdas')}</h3>
            <form_1.default model={this.model} hideFooter>
              <StyledSentryProjectSelectorField placeholder={(0, locale_1.t)('Select a project')} name="projectId" projects={projects} inline={false} hasControlState flexibleControlStateSize stacked/>
              <alert_1.default type="info">
                {(0, locale_1.t)('Currently only supports Node and Python Lambda functions')}
              </alert_1.default>
            </form_1.default>
          </listItem_1.default>
        </StyledList>
        <mobx_react_1.Observer>
          {() => (<footerWithButtons_1.default buttonText={(0, locale_1.t)('Next')} onClick={this.handleSubmit} disabled={this.model.isSaving || !this.model.getValue('projectId')}/>)}
        </mobx_react_1.Observer>
      </React.Fragment>);
    }
}
exports.default = AwsLambdaProjectSelect;
const StyledList = (0, styled_1.default)(list_1.default) `
  padding: 100px 50px 50px 50px;
`;
const StyledSentryProjectSelectorField = (0, styled_1.default)(sentryProjectSelectorField_1.default) `
  padding: 0 0 ${(0, space_1.default)(2)} 0;
`;
//# sourceMappingURL=awsLambdaProjectSelect.jsx.map