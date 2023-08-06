Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/events/styles");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const localStorage_1 = (0, tslib_1.__importDefault)(require("app/utils/localStorage"));
class ReprocessedBox extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isBannerHidden: localStorage_1.default.getItem(this.getBannerUniqueId()) === 'true',
        };
        this.handleBannerDismiss = () => {
            localStorage_1.default.setItem(this.getBannerUniqueId(), 'true');
            this.setState({ isBannerHidden: true });
        };
    }
    getBannerUniqueId() {
        const { reprocessActivity } = this.props;
        const { id } = reprocessActivity;
        return `reprocessed-activity-${id}-banner-dismissed`;
    }
    renderMessage() {
        const { orgSlug, reprocessActivity, groupCount, groupId } = this.props;
        const { data } = reprocessActivity;
        const { eventCount, oldGroupId, newGroupId } = data;
        const reprocessedEventsRoute = `/organizations/${orgSlug}/issues/?query=reprocessing.original_issue_id:${oldGroupId}`;
        if (groupCount === 0) {
            return (0, locale_1.tct)('All events in this issue were moved during reprocessing. [link]', {
                link: (<link_1.default to={reprocessedEventsRoute}>
            {(0, locale_1.tn)('See %s new event', 'See %s new events', eventCount)}
          </link_1.default>),
            });
        }
        return (0, locale_1.tct)('Events in this issue were successfully reprocessed. [link]', {
            link: (<link_1.default to={reprocessedEventsRoute}>
          {newGroupId === Number(groupId)
                    ? (0, locale_1.tn)('See %s reprocessed event', 'See %s reprocessed events', eventCount)
                    : (0, locale_1.tn)('See %s new event', 'See %s new events', eventCount)}
        </link_1.default>),
        });
    }
    render() {
        const { isBannerHidden } = this.state;
        if (isBannerHidden) {
            return null;
        }
        const { className } = this.props;
        return (<styles_1.BannerContainer priority="success" className={className}>
        <StyledBannerSummary>
          <icons_1.IconCheckmark color="green300" isCircled/>
          <span>{this.renderMessage()}</span>
          <StyledIconClose color="green300" aria-label={(0, locale_1.t)('Dismiss')} isCircled onClick={this.handleBannerDismiss}/>
        </StyledBannerSummary>
      </styles_1.BannerContainer>);
    }
}
exports.default = ReprocessedBox;
const StyledBannerSummary = (0, styled_1.default)(styles_1.BannerSummary) `
  & > svg:last-child {
    margin-right: 0;
    margin-left: ${(0, space_1.default)(1)};
  }
`;
const StyledIconClose = (0, styled_1.default)(icons_1.IconClose) `
  cursor: pointer;
`;
//# sourceMappingURL=reprocessedBox.jsx.map