Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const author_1 = (0, tslib_1.__importDefault)(require("app/components/activity/author"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const clipboard_1 = (0, tslib_1.__importDefault)(require("app/components/clipboard"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
class EventUserFeedback extends react_1.Component {
    getUrl() {
        const { report, orgId, issueId } = this.props;
        return `/organizations/${orgId}/issues/${issueId}/events/${report.eventID}/`;
    }
    render() {
        const { className, report } = this.props;
        const user = report.user || {
            name: report.name,
            email: report.email,
            id: '',
            username: '',
            ip_address: '',
        };
        return (<div className={className}>
        <item_1.default date={report.dateCreated} author={{ type: 'user', user }} header={<div>
              <author_1.default>{report.name}</author_1.default>
              <clipboard_1.default value={report.email}>
                <Email>
                  {report.email}
                  <StyledIconCopy size="xs"/>
                </Email>
              </clipboard_1.default>
              {report.eventID && (<ViewEventLink to={this.getUrl()}>{(0, locale_1.t)('View event')}</ViewEventLink>)}
            </div>}>
          <p dangerouslySetInnerHTML={{
                __html: (0, utils_1.nl2br)((0, utils_1.escape)(report.comments)),
            }}/>
        </item_1.default>
      </div>);
    }
}
exports.default = EventUserFeedback;
const Email = (0, styled_1.default)('span') `
  font-size: ${p => p.theme.fontSizeSmall};
  font-weight: normal;
  cursor: pointer;
  margin-left: ${(0, space_1.default)(1)};
`;
const ViewEventLink = (0, styled_1.default)(link_1.default) `
  font-weight: 300;
  margin-left: ${(0, space_1.default)(1)};
  font-size: 0.9em;
`;
const StyledIconCopy = (0, styled_1.default)(icons_1.IconCopy) `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=userFeedback.jsx.map