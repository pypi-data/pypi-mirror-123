Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const deviceName_1 = require("app/components/deviceName");
const tagDistributionMeter_1 = (0, tslib_1.__importDefault)(require("app/components/tagDistributionMeter"));
class GroupTagDistributionMeter extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    shouldComponentUpdate(nextProps, nextState) {
        return (this.state.loading !== nextState.loading ||
            this.state.error !== nextState.error ||
            this.props.tag !== nextProps.tag ||
            this.props.name !== nextProps.name ||
            this.props.totalValues !== nextProps.totalValues ||
            this.props.topValues !== nextProps.topValues);
    }
    fetchData() {
        this.setState({
            loading: true,
            error: false,
        });
        (0, deviceName_1.loadDeviceListModule)()
            .then(iOSDeviceList => {
            this.setState({
                iOSDeviceList,
                error: false,
                loading: false,
            });
        })
            .catch(() => {
            this.setState({
                error: true,
                loading: false,
            });
        });
    }
    render() {
        const { organization, group, tag, totalValues, topValues } = this.props;
        const { loading, error, iOSDeviceList } = this.state;
        const url = `/organizations/${organization.slug}/issues/${group.id}/tags/${tag}/`;
        const segments = topValues
            ? topValues.map(value => (Object.assign(Object.assign({}, value), { name: iOSDeviceList
                    ? (0, deviceName_1.deviceNameMapper)(value.name || '', iOSDeviceList) || ''
                    : value.name, url })))
            : [];
        return (<tagDistributionMeter_1.default title={tag} totalValues={totalValues} isLoading={loading} hasError={error} segments={segments}/>);
    }
}
exports.default = GroupTagDistributionMeter;
//# sourceMappingURL=tagDistributionMeter.jsx.map