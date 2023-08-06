Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const qs = (0, tslib_1.__importStar)(require("query-string"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/actions/button"));
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const guid_1 = require("app/utils/guid");
const integrationUtil_1 = require("app/utils/integrationUtil");
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const textField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/textField"));
const footerWithButtons_1 = (0, tslib_1.__importDefault)(require("./components/footerWithButtons"));
const headerWithHelp_1 = (0, tslib_1.__importDefault)(require("./components/headerWithHelp"));
// let the browser generate and store the external ID
// this way the same user always has the same external ID if they restart the pipeline
const ID_NAME = 'AWS_EXTERNAL_ID';
const getAwsExternalId = () => {
    let awsExternalId = window.localStorage.getItem(ID_NAME);
    if (!awsExternalId) {
        awsExternalId = (0, guid_1.uniqueId)();
        window.localStorage.setItem(ID_NAME, awsExternalId);
    }
    return awsExternalId;
};
const accountNumberRegex = /^\d{12}$/;
const testAccountNumber = (arn) => accountNumberRegex.test(arn);
class AwsLambdaCloudformation extends React.Component {
    constructor() {
        var _a;
        super(...arguments);
        this.state = {
            accountNumber: this.props.accountNumber,
            region: this.props.region,
            awsExternalId: (_a = this.props.awsExternalId) !== null && _a !== void 0 ? _a : getAwsExternalId(),
            showInputs: !!this.props.awsExternalId,
        };
        this.handleSubmit = (e) => {
            this.setState({ submitting: true });
            e.preventDefault();
            // use the external ID from the form on on the submission
            const { accountNumber, region, awsExternalId } = this.state;
            const data = {
                accountNumber,
                region,
                awsExternalId,
            };
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Submitting\u2026'));
            const { location: { origin }, } = window;
            // redirect to the extensions endpoint with the form fields as query params
            // this is needed so we don't restart the pipeline loading from the original
            // OrganizationIntegrationSetupView route
            const newUrl = `${origin}/extensions/aws_lambda/setup/?${qs.stringify(data)}`;
            window.location.assign(newUrl);
        };
        this.validateAccountNumber = (value) => {
            // validate the account number
            let accountNumberError = '';
            if (!value) {
                accountNumberError = (0, locale_1.t)('Account number required');
            }
            else if (!testAccountNumber(value)) {
                accountNumberError = (0, locale_1.t)('Invalid account number');
            }
            this.setState({ accountNumberError });
        };
        this.handleChangeArn = (accountNumber) => {
            this.debouncedTrackValueChanged('accountNumber');
            // reset the error if we ever get a valid account number
            if (testAccountNumber(accountNumber)) {
                this.setState({ accountNumberError: '' });
            }
            this.setState({ accountNumber });
        };
        this.handleChangeRegion = (region) => {
            this.debouncedTrackValueChanged('region');
            this.setState({ region });
        };
        this.handleChangeExternalId = (awsExternalId) => {
            this.debouncedTrackValueChanged('awsExternalId');
            awsExternalId = awsExternalId.trim();
            this.setState({ awsExternalId });
        };
        this.handleChangeShowInputs = () => {
            this.setState({ showInputs: true });
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_input_value_changed', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
                field_name: 'showInputs',
                organization: this.props.organization,
            });
        };
        // debounce so we don't send a request on every input change
        this.debouncedTrackValueChanged = (0, debounce_1.default)((fieldName) => {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.installation_input_value_changed', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
                field_name: fieldName,
                organization: this.props.organization,
            });
        }, 200);
        this.trackOpenCloudFormation = () => {
            (0, integrationUtil_1.trackIntegrationAnalytics)('integrations.cloudformation_link_clicked', {
                integration: 'aws_lambda',
                integration_type: 'first_party',
                organization: this.props.organization,
            });
        };
        this.render = () => {
            const { initialStepNumber } = this.props;
            const { accountNumber, region, accountNumberError, submitting, awsExternalId, showInputs, } = this.state;
            return (<React.Fragment>
        <headerWithHelp_1.default docsUrl="https://docs.sentry.io/product/integrations/cloud-monitoring/aws-lambda/"/>
        <StyledList symbol="colored-numeric" initialCounterValue={initialStepNumber}>
          <listItem_1.default>
            <h3>{(0, locale_1.t)("Add Sentry's CloudFormation")}</h3>
            <StyledButton priority="primary" onClick={this.trackOpenCloudFormation} external href={this.cloudformationUrl}>
              {(0, locale_1.t)('Go to AWS')}
            </StyledButton>
            {!showInputs && (<React.Fragment>
                <p>
                  {(0, locale_1.t)("Once you've created Sentry's CloudFormation stack (or if you already have one) press the button below to continue.")}
                </p>
                <button_1.default name="showInputs" onClick={this.handleChangeShowInputs}>
                  {(0, locale_1.t)("I've created the stack")}
                </button_1.default>
              </React.Fragment>)}
          </listItem_1.default>
          {showInputs ? (<listItem_1.default>
              <h3>{(0, locale_1.t)('Add AWS Account Information')}</h3>
              <textField_1.default name="accountNumber" value={accountNumber} onChange={this.handleChangeArn} onBlur={this.validateAccountNumber} error={accountNumberError} inline={false} stacked label={(0, locale_1.t)('AWS Account Number')} showHelpInTooltip help={(0, locale_1.t)('Your account number can be found on the right side of the header in AWS')}/>
              <selectField_1.default name="region" value={region} onChange={this.handleChangeRegion} options={this.regionOptions} allowClear={false} inline={false} stacked label={(0, locale_1.t)('AWS Region')} showHelpInTooltip help={(0, locale_1.t)('Your current region can be found on the right side of the header in AWS')}/>
              <textField_1.default name="awsExternalId" value={awsExternalId} onChange={this.handleChangeExternalId} inline={false} stacked error={awsExternalId ? '' : (0, locale_1.t)('External ID Required')} label={(0, locale_1.t)('External ID')} showHelpInTooltip help={(0, locale_1.t)('Do not edit unless you are copying from a previously created CloudFormation stack')}/>
            </listItem_1.default>) : (<React.Fragment />)}
        </StyledList>
        <footerWithButtons_1.default buttonText={(0, locale_1.t)('Next')} onClick={this.handleSubmit} disabled={submitting || !this.formValid}/>
      </React.Fragment>);
        };
    }
    componentDidMount() {
        // show the error if we have it
        const { error } = this.props;
        if (error) {
            (0, indicator_1.addErrorMessage)(error, { duration: 10000 });
        }
    }
    get initialData() {
        const { region, accountNumber } = this.props;
        const { awsExternalId } = this.state;
        return {
            awsExternalId,
            region,
            accountNumber,
        };
    }
    get cloudformationUrl() {
        // generate the cloudformation URL using the params we get from the server
        // and the external id we generate
        const { baseCloudformationUrl, templateUrl, stackName } = this.props;
        // always us the generated AWS External ID in local storage
        const awsExternalId = getAwsExternalId();
        const query = qs.stringify({
            templateURL: templateUrl,
            stackName,
            param_ExternalId: awsExternalId,
        });
        return `${baseCloudformationUrl}?${query}`;
    }
    get regionOptions() {
        return this.props.regionList.map(region => ({ value: region, label: region }));
    }
    get formValid() {
        const { accountNumber, region, awsExternalId } = this.state;
        return !!region && testAccountNumber(accountNumber || '') && !!awsExternalId;
    }
}
exports.default = AwsLambdaCloudformation;
const StyledList = (0, styled_1.default)(list_1.default) `
  padding: 100px 50px 50px 50px;
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin-bottom: 20px;
`;
//# sourceMappingURL=awsLambdaCloudformation.jsx.map