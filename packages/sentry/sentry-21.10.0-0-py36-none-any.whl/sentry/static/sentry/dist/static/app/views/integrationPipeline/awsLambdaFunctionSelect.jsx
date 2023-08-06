Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const reduce_1 = (0, tslib_1.__importDefault)(require("lodash/reduce"));
const mobx_1 = require("mobx");
const mobx_react_1 = require("mobx-react");
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const switchButton_1 = (0, tslib_1.__importDefault)(require("app/components/switchButton"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const locale_1 = require("app/locale");
const form_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/form"));
const jsonForm_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/jsonForm"));
const model_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/model"));
const footerWithButtons_1 = (0, tslib_1.__importDefault)(require("./components/footerWithButtons"));
const headerWithHelp_1 = (0, tslib_1.__importDefault)(require("./components/headerWithHelp"));
const LAMBDA_COUNT_THRESHOLD = 10;
const getLabel = (func) => func.FunctionName;
class AwsLambdaFunctionSelect extends react_1.Component {
    constructor(props) {
        super(props);
        this.state = {
            submitting: false,
        };
        this.model = new model_1.default({ apiOptions: { baseUrl: window.location.origin } });
        this.handleSubmit = () => {
            this.model.saveForm();
            this.setState({ submitting: true });
        };
        this.handleToggle = () => {
            const newState = !this.allStatesToggled;
            this.lambdaFunctions.forEach(lambda => {
                this.model.setValue(lambda.FunctionName, newState, { quiet: true });
            });
        };
        this.renderWhatWeFound = () => {
            const count = this.lambdaFunctions.length;
            return (<h4>
        {(0, locale_1.tn)('We found %s function with a Node or Python runtime', 'We found %s functions with Node or Python runtimes', count)}
      </h4>);
        };
        this.renderLoadingScreen = () => {
            const count = this.enabledCount;
            const text = count > LAMBDA_COUNT_THRESHOLD
                ? (0, locale_1.t)('This might take a while\u2026', count)
                : (0, locale_1.t)('This might take a sec\u2026');
            return (<LoadingWrapper>
        <StyledLoadingIndicator />
        <h4>{(0, locale_1.t)('Adding Sentry to %s functions', count)}</h4>
        {text}
      </LoadingWrapper>);
        };
        this.renderCore = () => {
            const { initialStepNumber } = this.props;
            const FormHeader = (<StyledPanelHeader>
        {(0, locale_1.t)('Lambda Functions')}
        <SwitchHolder>
          <mobx_react_1.Observer>
            {() => (<tooltip_1.default title={this.allStatesToggled ? (0, locale_1.t)('Disable All') : (0, locale_1.t)('Enable All')} position="left">
                <StyledSwitch size="lg" name="toggleAll" toggle={this.handleToggle} isActive={this.allStatesToggled}/>
              </tooltip_1.default>)}
          </mobx_react_1.Observer>
        </SwitchHolder>
      </StyledPanelHeader>);
            const formFields = {
                fields: this.lambdaFunctions.map(func => ({
                    name: func.FunctionName,
                    type: 'boolean',
                    required: false,
                    label: getLabel(func),
                    alignRight: true,
                })),
            };
            return (<list_1.default symbol="colored-numeric" initialCounterValue={initialStepNumber}>
        <listItem_1.default>
          <Header>{this.renderWhatWeFound()}</Header>
          {(0, locale_1.t)('Decide which functions you would like to enable for Sentry monitoring')}
          <StyledForm initialData={this.initialData} skipPreventDefault model={this.model} apiEndpoint="/extensions/aws_lambda/setup/" hideFooter>
            <jsonForm_1.default renderHeader={() => FormHeader} forms={[formFields]}/>
          </StyledForm>
        </listItem_1.default>
        <react_1.Fragment />
      </list_1.default>);
        };
        (0, mobx_1.makeObservable)(this, { allStatesToggled: mobx_1.computed });
    }
    get initialData() {
        const { lambdaFunctions } = this.props;
        const initialData = lambdaFunctions.reduce((accum, func) => {
            accum[func.FunctionName] = true;
            return accum;
        }, {});
        return initialData;
    }
    get lambdaFunctions() {
        return this.props.lambdaFunctions.sort((a, b) => getLabel(a).toLowerCase() < getLabel(b).toLowerCase() ? -1 : 1);
    }
    get enabledCount() {
        const data = this.model.getTransformedData();
        return (0, reduce_1.default)(data, (acc, val) => (val ? acc + 1 : acc), 0);
    }
    get allStatesToggled() {
        // check if any of the lambda functions have a falsy value
        // no falsy values means everything is enabled
        return Object.values(this.model.getData()).every(val => val);
    }
    render() {
        return (<react_1.Fragment>
        <headerWithHelp_1.default docsUrl="https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/"/>
        <Wrapper>
          {this.state.submitting ? this.renderLoadingScreen() : this.renderCore()}
        </Wrapper>
        <mobx_react_1.Observer>
          {() => (<footerWithButtons_1.default buttonText={(0, locale_1.t)('Finish Setup')} onClick={this.handleSubmit} disabled={this.model.isError || this.model.isSaving}/>)}
        </mobx_react_1.Observer>
      </react_1.Fragment>);
    }
}
exports.default = AwsLambdaFunctionSelect;
const Wrapper = (0, styled_1.default)('div') `
  padding: 100px 50px 50px 50px;
`;
// TODO(ts): Understand why styled is not correctly inheriting props here
const StyledForm = (0, styled_1.default)(form_1.default) `
  margin-top: 10px;
`;
const Header = (0, styled_1.default)('div') `
  text-align: left;
  margin-bottom: 10px;
`;
const LoadingWrapper = (0, styled_1.default)('div') `
  padding: 50px;
  text-align: center;
`;
const StyledLoadingIndicator = (0, styled_1.default)(loadingIndicator_1.default) `
  margin: 0;
`;
const SwitchHolder = (0, styled_1.default)('div') `
  display: flex;
`;
const StyledSwitch = (0, styled_1.default)(switchButton_1.default) `
  margin: auto;
`;
// padding is based on fom control width
const StyledPanelHeader = (0, styled_1.default)(panels_1.PanelHeader) `
  padding-right: 36px;
`;
//# sourceMappingURL=awsLambdaFunctionSelect.jsx.map