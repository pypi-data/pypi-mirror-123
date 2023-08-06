Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const locale_1 = require("app/locale");
const dynamicSampling_1 = require("app/types/dynamicSampling");
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const permissionAlert_1 = (0, tslib_1.__importDefault)(require("app/views/settings/organization/permissionAlert"));
const utils_1 = require("./modal/utils");
const modal_2 = (0, tslib_1.__importDefault)(require("./modal"));
const rulesPanel_1 = (0, tslib_1.__importDefault)(require("./rulesPanel"));
const utils_2 = require("./utils");
class FiltersAndSampling extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.successfullySubmitted = (projectDetails, successMessage) => {
            this.setState({ projectDetails });
            if (successMessage) {
                (0, indicator_1.addSuccessMessage)(successMessage);
            }
        };
        this.handleOpenRule = (type, rule) => () => {
            const { organization, project } = this.props;
            const { errorRules, transactionRules } = this.state;
            return (0, modal_1.openModal)(modalProps => (<modal_2.default {...modalProps} type={type} api={this.api} organization={organization} project={project} rule={rule} errorRules={errorRules} transactionRules={transactionRules} onSubmitSuccess={this.successfullySubmitted}/>), {
                modalCss: utils_1.modalCss,
            });
        };
        this.handleAddRule = (type) => () => {
            if (type === 'errorRules') {
                this.handleOpenRule('error')();
                return;
            }
            this.handleOpenRule('transaction')();
        };
        this.handleEditRule = (rule) => () => {
            if (rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR) {
                this.handleOpenRule('error', rule)();
                return;
            }
            this.handleOpenRule('transaction', rule)();
        };
        this.handleDeleteRule = (rule) => () => {
            const { errorRules, transactionRules } = this.state;
            const newErrorRules = rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR
                ? errorRules.filter(errorRule => errorRule.id !== rule.id)
                : errorRules;
            const newTransactionRules = rule.type !== dynamicSampling_1.DynamicSamplingRuleType.ERROR
                ? transactionRules.filter(transactionRule => transactionRule.id !== rule.id)
                : transactionRules;
            const newRules = [...newErrorRules, ...newTransactionRules];
            this.submitRules(newRules, (0, locale_1.t)('Successfully deleted dynamic sampling rule'), (0, locale_1.t)('An error occurred while deleting dynamic sampling rule'));
        };
        this.handleUpdateRules = (rules) => {
            var _a;
            if (!rules.length) {
                return;
            }
            const { errorRules, transactionRules } = this.state;
            if (((_a = rules[0]) === null || _a === void 0 ? void 0 : _a.type) === dynamicSampling_1.DynamicSamplingRuleType.ERROR) {
                this.submitRules([...rules, ...transactionRules]);
                return;
            }
            this.submitRules([...errorRules, ...rules]);
        };
    }
    getTitle() {
        return (0, locale_1.t)('Filters & Sampling');
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { errorRules: [], transactionRules: [], projectDetails: null });
    }
    getEndpoints() {
        const { organization, project } = this.props;
        return [['projectDetails', `/projects/${organization.slug}/${project.slug}/`]];
    }
    componentDidMount() {
        this.getRules();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.projectDetails !== this.state.projectDetails) {
            this.getRules();
            return;
        }
    }
    getRules() {
        var _a;
        const { projectDetails } = this.state;
        if (!projectDetails) {
            return;
        }
        const { dynamicSampling } = projectDetails;
        const rules = (_a = dynamicSampling === null || dynamicSampling === void 0 ? void 0 : dynamicSampling.rules) !== null && _a !== void 0 ? _a : [];
        const [errorRules, transactionRules] = (0, partition_1.default)(rules, rule => rule.type === dynamicSampling_1.DynamicSamplingRuleType.ERROR);
        this.setState({ errorRules, transactionRules });
    }
    submitRules(newRules, successMessage, errorMessage) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, project } = this.props;
            try {
                const projectDetails = yield this.api.requestPromise(`/projects/${organization.slug}/${project.slug}/`, { method: 'PUT', data: { dynamicSampling: { rules: newRules } } });
                this.successfullySubmitted(projectDetails, successMessage);
            }
            catch (error) {
                this.getRules();
                if (errorMessage) {
                    (0, indicator_1.addErrorMessage)(errorMessage);
                }
            }
        });
    }
    renderBody() {
        const { errorRules, transactionRules } = this.state;
        const { hasAccess } = this.props;
        const disabled = !hasAccess;
        const hasNotSupportedConditionOperator = [...errorRules, ...transactionRules].some(rule => rule.condition.op !== dynamicSampling_1.DynamicSamplingConditionOperator.AND);
        if (hasNotSupportedConditionOperator) {
            return (<alert_1.default type="error">
          {(0, locale_1.t)('A condition operator has been found that is not yet supported.')}
        </alert_1.default>);
        }
        return (<React.Fragment>
        <settingsPageHeader_1.default title={this.getTitle()}/>
        <permissionAlert_1.default />
        <textBlock_1.default>
          {(0, locale_1.tct)('Manage the inbound data you want to store. To change the sampling rate or rate limits, [link:update your SDK configuration]. The rules added below will apply on top of your SDK configuration. Any new rule may take a few minutes to propagate.', {
                link: <externalLink_1.default href={utils_2.DYNAMIC_SAMPLING_DOC_LINK}/>,
            })}
        </textBlock_1.default>
        <rulesPanel_1.default rules={errorRules} disabled={disabled} onAddRule={this.handleAddRule('errorRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules} isErrorPanel/>
        <textBlock_1.default>
          {(0, locale_1.t)('Rules for traces should precede rules for individual transactions.')}
        </textBlock_1.default>
        <rulesPanel_1.default rules={transactionRules} disabled={disabled} onAddRule={this.handleAddRule('transactionRules')} onEditRule={this.handleEditRule} onDeleteRule={this.handleDeleteRule} onUpdateRules={this.handleUpdateRules}/>
      </React.Fragment>);
    }
}
exports.default = (0, withProject_1.default)(FiltersAndSampling);
//# sourceMappingURL=filtersAndSampling.jsx.map