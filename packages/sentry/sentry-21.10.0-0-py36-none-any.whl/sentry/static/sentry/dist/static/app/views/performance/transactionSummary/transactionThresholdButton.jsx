Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const transactionThresholdModal_1 = (0, tslib_1.__importStar)(require("./transactionThresholdModal"));
class TransactionThresholdButton extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            transactionThreshold: undefined,
            transactionThresholdMetric: undefined,
            loadingThreshold: false,
        };
        this.fetchTransactionThreshold = () => {
            const { api, organization, transactionName } = this.props;
            const project = this.getProject();
            if (!(0, utils_1.defined)(project)) {
                return;
            }
            const transactionThresholdUrl = `/organizations/${organization.slug}/project-transaction-threshold-override/`;
            this.setState({ loadingThreshold: true });
            api
                .requestPromise(transactionThresholdUrl, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: project.id,
                    transaction: transactionName,
                },
            })
                .then(([data]) => {
                this.setState({
                    loadingThreshold: false,
                    transactionThreshold: data.threshold,
                    transactionThresholdMetric: data.metric,
                });
            })
                .catch(() => {
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
                        loadingThreshold: false,
                        transactionThreshold: data.threshold,
                        transactionThresholdMetric: data.metric,
                    });
                })
                    .catch(err => {
                    var _a, _b;
                    this.setState({ loadingThreshold: false });
                    const errorMessage = (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.threshold) !== null && _b !== void 0 ? _b : null;
                    (0, indicator_1.addErrorMessage)(errorMessage);
                });
            });
        };
    }
    componentDidMount() {
        this.fetchTransactionThreshold();
    }
    getProject() {
        const { projects, eventView } = this.props;
        if (!(0, utils_1.defined)(eventView)) {
            return undefined;
        }
        const projectId = String(eventView.project[0]);
        const project = projects.find(proj => proj.id === projectId);
        return project;
    }
    onChangeThreshold(threshold, metric) {
        const { onChangeThreshold } = this.props;
        this.setState({
            transactionThreshold: threshold,
            transactionThresholdMetric: metric,
        });
        if ((0, utils_1.defined)(onChangeThreshold)) {
            onChangeThreshold(threshold, metric);
        }
    }
    openModal() {
        const { organization, transactionName, eventView } = this.props;
        const { transactionThreshold, transactionThresholdMetric } = this.state;
        (0, modal_1.openModal)(modalProps => (<transactionThresholdModal_1.default {...modalProps} organization={organization} transactionName={transactionName} eventView={eventView} transactionThreshold={transactionThreshold} transactionThresholdMetric={transactionThresholdMetric} onApply={(threshold, metric) => this.onChangeThreshold(threshold, metric)}/>), { modalCss: transactionThresholdModal_1.modalCss, backdrop: 'static' });
    }
    render() {
        const { loadingThreshold } = this.state;
        return (<button_1.default onClick={() => this.openModal()} icon={<icons_1.IconSettings />} disabled={loadingThreshold} aria-label={(0, locale_1.t)('Settings')} data-test-id="set-transaction-threshold"/>);
    }
}
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(TransactionThresholdButton));
//# sourceMappingURL=transactionThresholdButton.jsx.map