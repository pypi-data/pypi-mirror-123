Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const styles_1 = require("app/components/charts/styles");
const times_1 = (0, tslib_1.__importDefault)(require("app/components/group/times"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const seenByList_1 = (0, tslib_1.__importDefault)(require("app/components/seenByList"));
const shortId_1 = (0, tslib_1.__importDefault)(require("app/components/shortId"));
const groupChart_1 = (0, tslib_1.__importDefault)(require("app/components/stream/groupChart"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class LinkedIssue extends asyncComponent_1.default {
    getEndpoints() {
        const { groupId } = this.props;
        const groupUrl = `/issues/${groupId}/`;
        return [['group', groupUrl]];
    }
    renderLoading() {
        return <placeholder_1.default height="120px" bottomGutter={2}/>;
    }
    renderError(error, disableLog = false, disableReport = false) {
        const { errors } = this.state;
        const hasNotFound = Object.values(errors).find(resp => resp && resp.status === 404);
        if (hasNotFound) {
            return (<alert_1.default type="warning" icon={<icons_1.IconWarning size="md"/>}>
          {(0, locale_1.t)('The linked issue cannot be found. It may have been deleted, or merged.')}
        </alert_1.default>);
        }
        return super.renderError(error, disableLog, disableReport);
    }
    renderBody() {
        const { eventId } = this.props;
        const { group } = this.state;
        const issueUrl = `${group.permalink}events/${eventId}/`;
        return (<Section>
        <styles_1.SectionHeading>{(0, locale_1.t)('Event Issue')}</styles_1.SectionHeading>
        <StyledIssueCard>
          <IssueCardHeader>
            <StyledLink to={issueUrl} data-test-id="linked-issue">
              <StyledShortId shortId={group.shortId} avatar={<projectBadge_1.default project={group.project} avatarSize={16} hideName disableLink/>}/>
            </StyledLink>
            <StyledSeenByList seenBy={group.seenBy} maxVisibleAvatars={5}/>
          </IssueCardHeader>
          <IssueCardBody>
            <groupChart_1.default statsPeriod="30d" data={group} height={56}/>
          </IssueCardBody>
          <IssueCardFooter>
            <times_1.default lastSeen={group.lastSeen} firstSeen={group.firstSeen}/>
          </IssueCardFooter>
        </StyledIssueCard>
      </Section>);
    }
}
const Section = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(4)};
`;
const StyledIssueCard = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  border-radius: ${p => p.theme.borderRadius};
`;
const IssueCardHeader = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${(0, space_1.default)(1)};
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  justify-content: flex-start;
`;
const IssueCardBody = (0, styled_1.default)('div') `
  background: ${p => p.theme.backgroundSecondary};
  padding-top: ${(0, space_1.default)(1)};
`;
const StyledSeenByList = (0, styled_1.default)(seenByList_1.default) `
  margin: 0;
`;
const StyledShortId = (0, styled_1.default)(shortId_1.default) `
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.textColor};
`;
const IssueCardFooter = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeSmall};
  padding: ${(0, space_1.default)(0.5)} ${(0, space_1.default)(1)};
`;
exports.default = LinkedIssue;
//# sourceMappingURL=linkedIssue.jsx.map