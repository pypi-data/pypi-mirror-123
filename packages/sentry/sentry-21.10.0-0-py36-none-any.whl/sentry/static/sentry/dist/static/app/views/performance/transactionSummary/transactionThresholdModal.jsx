Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = exports.METRIC_CHOICES = exports.TransactionThresholdMetric = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const indicator_1 = require("app/actionCreators/indicator");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
const utils_2 = require("./utils");
var TransactionThresholdMetric;
(function (TransactionThresholdMetric) {
    TransactionThresholdMetric["TRANSACTION_DURATION"] = "duration";
    TransactionThresholdMetric["LARGEST_CONTENTFUL_PAINT"] = "lcp";
})(TransactionThresholdMetric = exports.TransactionThresholdMetric || (exports.TransactionThresholdMetric = {}));
exports.METRIC_CHOICES = [
    { label: (0, locale_1.t)('Transaction Duration'), value: 'duration' },
    { label: (0, locale_1.t)('Largest Contentful Paint'), value: 'lcp' },
];
class TransactionThresholdModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            threshold: this.props.transactionThreshold,
            metric: this.props.transactionThresholdMetric,
            error: null,
        };
        this.handleApply = (event) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            event.preventDefault();
            const { api, closeModal, organization, transactionName, onApply } = this.props;
            const project = this.getProject();
            if (!(0, utils_1.defined)(project)) {
                return;
            }
            const transactionThresholdUrl = `/organizations/${organization.slug}/project-transaction-threshold-override/`;
            api
                .requestPromise(transactionThresholdUrl, {
                method: 'POST',
                includeAllArgs: true,
                query: {
                    project: project.id,
                },
                data: {
                    transaction: transactionName,
                    threshold: this.state.threshold,
                    metric: this.state.metric,
                },
            })
                .then(() => {
                closeModal();
                if (onApply) {
                    onApply(this.state.threshold, this.state.metric);
                }
            })
                .catch(err => {
                var _a, _b, _c, _d;
                this.setState({
                    error: err,
                });
                const errorMessage = (_d = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.non_field_errors) !== null && _d !== void 0 ? _d : null;
                (0, indicator_1.addErrorMessage)(errorMessage);
            });
        });
        this.handleFieldChange = (field) => (value) => {
            this.setState(prevState => {
                const newState = (0, cloneDeep_1.default)(prevState);
                (0, set_1.default)(newState, field, value);
                return Object.assign(Object.assign({}, newState), { errors: undefined });
            });
        };
        this.handleReset = (event) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            event.preventDefault();
            const { api, closeModal, organization, transactionName, onApply } = this.props;
            const project = this.getProject();
            if (!(0, utils_1.defined)(project)) {
                return;
            }
            const transactionThresholdUrl = `/organizations/${organization.slug}/project-transaction-threshold-override/`;
            api
                .requestPromise(transactionThresholdUrl, {
                method: 'DELETE',
                includeAllArgs: true,
                query: {
                    project: project.id,
                },
                data: {
                    transaction: transactionName,
                },
            })
                .then(() => {
                const projectThresholdUrl = `/projects/${organization.slug}/${project.slug}/transaction-threshold/configure/`;
                this.props.api
                    .requestPromise(projectThresholdUrl, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: {
                        project: project.id,
                    },
                })
                    .then(([data]) => {
                    this.setState({
                        threshold: data.threshold,
                        metric: data.metric,
                    });
                    closeModal();
                    if (onApply) {
                        onApply(this.state.threshold, this.state.metric);
                    }
                })
                    .catch(err => {
                    var _a, _b;
                    const errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                    (0, indicator_1.addErrorMessage)(errorMessage);
                });
            })
                .catch(err => {
                this.setState({
                    error: err,
                });
            });
        });
    }
    getProject() {
        const { projects, eventView, project } = this.props;
        if ((0, utils_1.defined)(project)) {
            return projects.find(proj => proj.id === project);
        }
        else {
            const projectId = String(eventView.project[0]);
            return projects.find(proj => proj.id === projectId);
        }
    }
    renderModalFields() {
        return (<React.Fragment>
        <field_1.default data-test-id="response-metric" label={(0, locale_1.t)('Calculation Method')} inline={false} help={(0, locale_1.t)('This determines which duration metric is used for the Response Time Threshold.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <selectControl_1.default required options={exports.METRIC_CHOICES.slice()} name="responseMetric" label={(0, locale_1.t)('Calculation Method')} value={this.state.metric} onChange={(option) => {
                this.handleFieldChange('metric')(option.value);
            }}/>
        </field_1.default>
        <field_1.default data-test-id="response-time-threshold" label={(0, locale_1.t)('Response Time Threshold (ms)')} inline={false} help={(0, locale_1.t)('The satisfactory response time for the calculation method defined above. This is used to calculate Apdex and User Misery scores.')} showHelpInTooltip flexibleControlStateSize stacked required>
          <input_1.default type="number" name="threshold" required pattern="[0-9]*(\.[0-9]*)?" onChange={(event) => {
                this.handleFieldChange('threshold')(event.target.value);
            }} value={this.state.threshold} step={100} min={100}/>
        </field_1.default>
      </React.Fragment>);
    }
    render() {
        const { Header, Body, Footer, organization, transactionName, eventView } = this.props;
        const project = this.getProject();
        const summaryView = eventView.clone();
        summaryView.query = summaryView.getQueryWithAdditionalConditions();
        const target = (0, utils_2.transactionSummaryRouteWithQuery)({
            orgSlug: organization.slug,
            transaction: transactionName,
            query: summaryView.generateQueryStringObject(),
            projectID: project === null || project === void 0 ? void 0 : project.id,
        });
        return (<React.Fragment>
        <Header closeButton>
          <h4>{(0, locale_1.t)('Transaction Settings')}</h4>
        </Header>
        <Body>
          <Instruction>
            {(0, locale_1.tct)('The changes below will only be applied to [transaction]. To set it at a more global level, go to [projectSettings: Project Settings].', {
                transaction: <link_1.default to={target}>{transactionName}</link_1.default>,
                projectSettings: (<link_1.default to={`/settings/${organization.slug}/projects/${project === null || project === void 0 ? void 0 : project.slug}/performance/`}/>),
            })}
          </Instruction>
          {this.renderModalFields()}
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default priority="default" onClick={this.handleReset} data-test-id="reset-all">
              {(0, locale_1.t)('Reset All')}
            </button_1.default>
            <button_1.default label={(0, locale_1.t)('Apply')} priority="primary" onClick={this.handleApply} data-test-id="apply-threshold">
              {(0, locale_1.t)('Apply')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    }
}
const Instruction = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
`;
exports.modalCss = (0, react_1.css) `
  width: 100%;
  max-width: 650px;
  margin: 70px auto;
`;
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(TransactionThresholdModal));
//# sourceMappingURL=transactionThresholdModal.jsx.map