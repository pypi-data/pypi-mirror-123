Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const chart_1 = (0, tslib_1.__importDefault)(require("./chart"));
const statsRequest_1 = (0, tslib_1.__importDefault)(require("./statsRequest"));
function Card({ widget, api, location, router, organization, project, selection }) {
    const { groupings, searchQuery, title, displayType } = widget;
    return (<errorBoundary_1.default customComponent={<ErrorCard>{(0, locale_1.t)('Error loading widget data')}</ErrorCard>}>
      <StyledPanel>
        <Title>{title}</Title>
        <statsRequest_1.default api={api} location={location} organization={organization} projectSlug={project.slug} groupings={groupings} searchQuery={searchQuery} environments={selection.environments} datetime={selection.datetime}>
          {({ isLoading, errored, series }) => {
            return (<chart_1.default displayType={displayType} series={series} isLoading={isLoading} errored={errored} location={location} platform={project.platform} selection={selection} router={router}/>);
        }}
        </statsRequest_1.default>
      </StyledPanel>
    </errorBoundary_1.default>);
}
exports.default = Card;
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  margin: 0;
  /* If a panel overflows due to a long title stretch its grid sibling */
  height: 100%;
  min-height: 96px;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)};
`;
const ErrorCard = (0, styled_1.default)(placeholder_1.default) `
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: ${p => p.theme.alert.error.backgroundLight};
  border: 1px solid ${p => p.theme.alert.error.border};
  color: ${p => p.theme.alert.error.textLight};
  border-radius: ${p => p.theme.borderRadius};
  margin-bottom: ${(0, space_1.default)(2)};
`;
const Title = (0, styled_1.default)(styles_1.HeaderTitle) `
  ${overflowEllipsis_1.default};
`;
//# sourceMappingURL=card.jsx.map