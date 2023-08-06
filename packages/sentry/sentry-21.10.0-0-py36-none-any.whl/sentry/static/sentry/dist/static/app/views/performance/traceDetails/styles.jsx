Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = exports.ProjectBadgeContainer = exports.TracePanel = exports.TraceViewContainer = exports.TraceDetailBody = exports.TraceDetailHeader = exports.TraceViewHeaderContainer = exports.TraceSearchBar = exports.TraceSearchContainer = exports.TransactionDetailsContainer = exports.TransactionDetails = exports.Row = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const eventTagsPill_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventTags/eventTagsPill"));
const header_1 = require("app/components/events/interfaces/spans/header");
const panels_1 = require("app/components/panels");
const pills_1 = (0, tslib_1.__importDefault)(require("app/components/pills"));
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const queryString_1 = require("app/utils/queryString");
const utils_2 = require("app/views/performance/transactionSummary/utils");
var spanDetail_1 = require("app/components/events/interfaces/spans/spanDetail");
Object.defineProperty(exports, "Row", { enumerable: true, get: function () { return spanDetail_1.Row; } });
Object.defineProperty(exports, "TransactionDetails", { enumerable: true, get: function () { return spanDetail_1.SpanDetails; } });
Object.defineProperty(exports, "TransactionDetailsContainer", { enumerable: true, get: function () { return spanDetail_1.SpanDetailContainer; } });
exports.TraceSearchContainer = (0, styled_1.default)('div') `
  display: flex;
  width: 100%;
`;
exports.TraceSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
exports.TraceViewHeaderContainer = (0, styled_1.default)(header_1.SecondaryHeader) `
  position: static;
  top: auto;
  border-top: none;
  border-bottom: 1px solid ${p => p.theme.border};
`;
exports.TraceDetailHeader = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: minmax(250px, 1fr) minmax(160px, 1fr) 6fr;
    grid-row-gap: 0;
  }
`;
exports.TraceDetailBody = (0, styled_1.default)('div') `
  margin-top: ${(0, space_1.default)(2)};
`;
exports.TraceViewContainer = (0, styled_1.default)('div') `
  overflow-x: hidden;
  border-bottom-left-radius: 3px;
  border-bottom-right-radius: 3px;
`;
exports.TracePanel = (0, styled_1.default)(panels_1.Panel) `
  overflow: hidden;
`;
exports.ProjectBadgeContainer = (0, styled_1.default)('span') `
  margin-right: ${(0, space_1.default)(0.75)};
  display: flex;
  flex-direction: column;
  justify-content: center;
`;
const StyledPills = (0, styled_1.default)(pills_1.default) `
  padding-top: ${(0, space_1.default)(1.5)};
`;
function Tags({ location, organization, transaction, }) {
    const { tags } = transaction;
    if (!tags || tags.length <= 0) {
        return null;
    }
    const orgSlug = organization.slug;
    const releasesPath = `/organizations/${orgSlug}/releases/`;
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <StyledPills>
          {tags.map((tag, index) => {
            const { pathname: streamPath, query } = (0, utils_2.transactionSummaryRouteWithQuery)({
                orgSlug,
                transaction: transaction.transaction,
                projectID: String(transaction.project_id),
                query: Object.assign(Object.assign({}, location.query), { query: (0, queryString_1.appendTagCondition)(location.query.query, tag.key, tag.value) }),
            });
            return (<eventTagsPill_1.default key={!(0, utils_1.defined)(tag.key) ? `tag-pill-${index}` : tag.key} tag={tag} projectId={transaction.project_slug} organization={organization} query={query} streamPath={streamPath} releasesPath={releasesPath}/>);
        })}
        </StyledPills>
      </td>
    </tr>);
}
exports.Tags = Tags;
//# sourceMappingURL=styles.jsx.map