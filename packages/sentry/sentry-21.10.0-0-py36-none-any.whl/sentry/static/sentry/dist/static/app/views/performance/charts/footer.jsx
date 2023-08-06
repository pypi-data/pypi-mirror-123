Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const events_1 = require("app/actionCreators/events");
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const data_1 = require("../data");
class ChartFooter extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            totalValues: null,
        };
        this.shouldRefetchData = (prevProps) => {
            const thisAPIPayload = this.props.eventView.getEventsAPIPayload(this.props.location);
            const otherAPIPayload = prevProps.eventView.getEventsAPIPayload(prevProps.location);
            return !(0, eventView_1.isAPIPayloadSimilar)(thisAPIPayload, otherAPIPayload);
        };
        this.mounted = false;
    }
    componentDidMount() {
        this.mounted = true;
        this.fetchTotalCount();
    }
    componentDidUpdate(prevProps) {
        const orgSlugHasChanged = this.props.organization.slug !== prevProps.organization.slug;
        const shouldRefetch = this.shouldRefetchData(prevProps);
        if ((orgSlugHasChanged || shouldRefetch) && this.props.eventView.isValid()) {
            this.fetchTotalCount();
        }
    }
    componentWillUnmount() {
        this.mounted = false;
    }
    handleSelectorChange(key, value) {
        const { location, organization } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'performance_views.overview.change_chart',
            eventName: 'Performance Views: Change Overview Chart',
            organization_id: parseInt(organization.id, 10),
            metric: value,
        });
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { [key]: value }),
        });
    }
    fetchTotalCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, location, eventView } = this.props;
            if (!eventView.isValid() || !this.mounted) {
                return;
            }
            try {
                const totals = yield (0, events_1.fetchTotalCount)(api, organization.slug, eventView.getEventsAPIPayload(location));
                if (this.mounted) {
                    this.setState({ totalValues: totals });
                }
            }
            catch (err) {
                Sentry.captureException(err);
            }
        });
    }
    render() {
        const { leftAxis, organization, rightAxis } = this.props;
        const { totalValues } = this.state;
        const value = typeof totalValues === 'number' ? totalValues.toLocaleString() : '-';
        const options = this.props.options || (0, data_1.getAxisOptions)(organization);
        const leftOptions = options.map(opt => (Object.assign(Object.assign({}, opt), { disabled: opt.value === rightAxis })));
        const rightOptions = options.map(opt => (Object.assign(Object.assign({}, opt), { disabled: opt.value === leftAxis })));
        return (<styles_1.ChartControls>
        <styles_1.InlineContainer>
          <styles_1.SectionHeading>{(0, locale_1.t)('Total Events')}</styles_1.SectionHeading>
          <styles_1.SectionValue>{value}</styles_1.SectionValue>
        </styles_1.InlineContainer>
        <styles_1.InlineContainer>
          <optionSelector_1.default title={(0, locale_1.t)('Display 1')} selected={leftAxis} options={leftOptions} onChange={(val) => this.handleSelectorChange('left', val)}/>
          <optionSelector_1.default title={(0, locale_1.t)('Display 2')} selected={rightAxis} options={rightOptions} onChange={(val) => this.handleSelectorChange('right', val)}/>
        </styles_1.InlineContainer>
      </styles_1.ChartControls>);
    }
}
exports.default = ChartFooter;
//# sourceMappingURL=footer.jsx.map