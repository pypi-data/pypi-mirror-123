Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const events_1 = require("app/actionCreators/events");
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const styles_1 = require("app/components/charts/styles");
const emptyStateWarning_1 = (0, tslib_1.__importDefault)(require("app/components/emptyStateWarning"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const tagDistributionMeter_1 = (0, tslib_1.__importDefault)(require("app/components/tagDistributionMeter"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const eventView_1 = require("app/utils/discover/eventView");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class Tags extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            tags: [],
            totalValues: null,
            error: '',
        };
        this.shouldRefetchData = (prevProps) => {
            const thisAPIPayload = this.props.eventView.getFacetsAPIPayload(this.props.location);
            const otherAPIPayload = prevProps.eventView.getFacetsAPIPayload(prevProps.location);
            return !(0, eventView_1.isAPIPayloadSimilar)(thisAPIPayload, otherAPIPayload);
        };
        this.fetchData = (forceFetchData = false) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, eventView, location, confirmedQuery } = this.props;
            this.setState({ loading: true, error: '', tags: [] });
            // Fetch should be forced after mounting as confirmedQuery isn't guaranteed
            // since this component can mount/unmount via show/hide tags separate from
            // data being loaded for the rest of the page.
            if (!forceFetchData && confirmedQuery === false) {
                return;
            }
            try {
                const tags = yield (0, events_1.fetchTagFacets)(api, organization.slug, eventView.getFacetsAPIPayload(location));
                this.setState({ loading: false, tags });
            }
            catch (err) {
                Sentry.captureException(err);
                this.setState({ loading: false, error: err });
            }
        });
        this.handleTagClick = (tag) => {
            const { organization } = this.props;
            // metrics
            (0, analytics_1.trackAnalyticsEvent)({
                eventKey: 'discover_v2.facet_map.clicked',
                eventName: 'Discoverv2: Clicked on a tag on the facet map',
                tag,
                organization_id: parseInt(organization.id, 10),
            });
        };
        this.renderBody = () => {
            const { loading, error, tags } = this.state;
            if (loading) {
                return this.renderPlaceholders();
            }
            if (error) {
                return (<errorPanel_1.default height="132px">
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>);
            }
            if (tags.length > 0) {
                return tags.map(tag => this.renderTag(tag));
            }
            else {
                return (<StyledEmptyStateWarning small>{(0, locale_1.t)('No tags found')}</StyledEmptyStateWarning>);
            }
        };
    }
    componentDidMount() {
        this.fetchData(true);
    }
    componentDidUpdate(prevProps) {
        if (this.shouldRefetchData(prevProps) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    }
    renderTag(tag) {
        const { generateUrl, totalValues } = this.props;
        const segments = tag.topValues.map(segment => {
            segment.url = generateUrl(tag.key, segment.value);
            return segment;
        });
        // Ensure we don't show >100% if there's a slight mismatch between the facets
        // endpoint and the totals endpoint
        const maxTotalValues = segments.length > 0
            ? Math.max(Number(totalValues), segments[0].count)
            : totalValues;
        return (<tagDistributionMeter_1.default key={tag.key} title={tag.key} segments={segments} totalValues={Number(maxTotalValues)} renderLoading={() => <StyledPlaceholder height="16px"/>} onTagClick={this.handleTagClick} showReleasePackage/>);
    }
    renderPlaceholders() {
        return (<react_1.Fragment>
        <StyledPlaceholderTitle key="title-1"/>
        <StyledPlaceholder key="bar-1"/>
        <StyledPlaceholderTitle key="title-2"/>
        <StyledPlaceholder key="bar-2"/>
        <StyledPlaceholderTitle key="title-3"/>
        <StyledPlaceholder key="bar-3"/>
      </react_1.Fragment>);
    }
    render() {
        return (<react_1.Fragment>
        <styles_1.SectionHeading>{(0, locale_1.t)('Tag Summary')}</styles_1.SectionHeading>
        {this.renderBody()}
      </react_1.Fragment>);
    }
}
exports.Tags = Tags;
const StyledEmptyStateWarning = (0, styled_1.default)(emptyStateWarning_1.default) `
  height: 132px;
  padding: 54px 15%;
`;
const StyledPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  border-radius: ${p => p.theme.borderRadius};
  height: 16px;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const StyledPlaceholderTitle = (0, styled_1.default)(placeholder_1.default) `
  width: 100px;
  height: 12px;
  margin-bottom: ${(0, space_1.default)(0.5)};
`;
exports.default = (0, withApi_1.default)(Tags);
//# sourceMappingURL=tags.jsx.map