Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const classnames_1 = (0, tslib_1.__importDefault)(require("classnames"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const eventOrGroupTitle_1 = (0, tslib_1.__importDefault)(require("app/components/eventOrGroupTitle"));
const eventAnnotation_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventAnnotation"));
const eventMessage_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventMessage"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const events_1 = require("app/utils/events");
const IssueLink = ({ children, orgId, issue, to, card = true }) => {
    if (!card) {
        return <link_1.default to={to}>{children}</link_1.default>;
    }
    const message = (0, events_1.getMessage)(issue);
    const className = (0, classnames_1.default)({
        isBookmarked: issue.isBookmarked,
        hasSeen: issue.hasSeen,
        isResolved: issue.status === 'resolved',
    });
    const streamPath = `/organizations/${orgId}/issues/`;
    const hovercardBody = (<div className={className}>
      <Section>
        <Title>
          <eventOrGroupTitle_1.default data={issue}/>
        </Title>

        <HovercardEventMessage level={issue.level} levelIndicatorSize="9px" message={message} annotations={<React.Fragment>
              {issue.logger && (<eventAnnotation_1.default>
                  <link_1.default to={{
                    pathname: streamPath,
                    query: { query: `logger:${issue.logger}` },
                }}>
                    {issue.logger}
                  </link_1.default>
                </eventAnnotation_1.default>)}
              {issue.annotations.map((annotation, i) => (<eventAnnotation_1.default key={i} dangerouslySetInnerHTML={{ __html: annotation }}/>))}
            </React.Fragment>}/>
      </Section>

      <Grid>
        <div>
          <GridHeader>{(0, locale_1.t)('First Seen')}</GridHeader>
          <StyledTimeSince date={issue.firstSeen}/>
        </div>
        <div>
          <GridHeader>{(0, locale_1.t)('Last Seen')}</GridHeader>
          <StyledTimeSince date={issue.lastSeen}/>
        </div>
        <div>
          <GridHeader>{(0, locale_1.t)('Occurrences')}</GridHeader>
          <count_1.default value={issue.count}/>
        </div>
        <div>
          <GridHeader>{(0, locale_1.t)('Users Affected')}</GridHeader>
          <count_1.default value={issue.userCount}/>
        </div>
      </Grid>
    </div>);
    return (<hovercard_1.default body={hovercardBody} header={issue.shortId}>
      <link_1.default to={to}>{children}</link_1.default>
    </hovercard_1.default>);
};
exports.default = IssueLink;
const Title = (0, styled_1.default)('h3') `
  font-size: ${p => p.theme.fontSizeMedium};
  margin: 0 0 ${(0, space_1.default)(0.5)};
  ${overflowEllipsis_1.default};

  em {
    font-style: normal;
    font-weight: 400;
    color: ${p => p.theme.gray300};
    font-size: 90%;
  }
`;
const Section = (0, styled_1.default)('section') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const Grid = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-gap: ${(0, space_1.default)(2)};
`;
const HovercardEventMessage = (0, styled_1.default)(eventMessage_1.default) `
  font-size: 12px;
`;
const GridHeader = (0, styled_1.default)('h5') `
  color: ${p => p.theme.gray300};
  font-size: 11px;
  margin-bottom: ${(0, space_1.default)(0.5)};
  text-transform: uppercase;
`;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: inherit;
`;
//# sourceMappingURL=issueLink.jsx.map