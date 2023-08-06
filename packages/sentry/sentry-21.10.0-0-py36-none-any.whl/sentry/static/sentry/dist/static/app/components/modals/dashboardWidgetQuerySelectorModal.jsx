Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const utils_1 = require("app/views/dashboardsV2/utils");
const input_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/controls/input"));
class DashboardWidgetQuerySelectorModal extends React.Component {
    renderQueries() {
        const { organization, widget, selection } = this.props;
        const querySearchBars = widget.queries.map((query, index) => {
            const eventView = (0, utils_1.eventViewFromWidget)(widget.title, query, selection, widget.displayType);
            const discoverLocation = eventView.getResultsViewUrlTarget(organization.slug);
            // Pull a max of 3 valid Y-Axis from the widget
            const yAxisOptions = eventView.getYAxisOptions().map(({ value }) => value);
            discoverLocation.query.yAxis = query.fields
                .filter(field => yAxisOptions.includes(field))
                .slice(0, 3);
            return (<React.Fragment key={index}>
          <QueryContainer>
            <Container>
              <SearchLabel htmlFor="smart-search-input" aria-label={(0, locale_1.t)('Search events')}>
                <icons_1.IconSearch />
              </SearchLabel>
              <StyledInput value={query.conditions} disabled/>
            </Container>
            <OpenInDiscoverButton priority="primary" icon={<icons_1.IconChevron size="xs" direction="right"/>} onClick={() => {
                    (0, trackAdvancedAnalyticsEvent_1.default)('dashboards_views.query_selector.selected', {
                        organization,
                        widget_type: widget.displayType,
                    });
                    react_router_1.browserHistory.push(discoverLocation);
                }}/>
          </QueryContainer>
        </React.Fragment>);
        });
        return querySearchBars;
    }
    render() {
        const { Body, Header, widget } = this.props;
        return (<React.Fragment>
        <Header closeButton>
          <h4>{widget.title}</h4>
        </Header>
        <Body>
          <p>
            {(0, locale_1.t)('Multiple queries were used to create this widget visualization. Which query would you like to view in Discover?')}
          </p>
          {this.renderQueries()}
        </Body>
      </React.Fragment>);
    }
}
const StyledInput = (0, styled_1.default)(input_1.default) `
  text-overflow: ellipsis;
  padding: 0px;
  box-shadow: none;
  height: auto;
  &:disabled {
    border: none;
    cursor: default;
  }
`;
const QueryContainer = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const OpenInDiscoverButton = (0, styled_1.default)(button_1.default) `
  margin-left: ${(0, space_1.default)(1)};
`;
const Container = (0, styled_1.default)('div') `
  border: 1px solid ${p => p.theme.border};
  box-shadow: inset ${p => p.theme.dropShadowLight};
  background: ${p => p.theme.backgroundSecondary};
  padding: 7px ${(0, space_1.default)(1)};
  position: relative;
  display: grid;
  grid-template-columns: max-content 1fr max-content;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: start;
  flex-grow: 1;
  border-radius: ${p => p.theme.borderRadius};
`;
const SearchLabel = (0, styled_1.default)('label') `
  display: flex;
  padding: ${(0, space_1.default)(0.5)} 0;
  margin: 0;
  color: ${p => p.theme.gray300};
`;
exports.modalCss = (0, react_1.css) `
  width: 100%;
  max-width: 700px;
  margin: 70px auto;
`;
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)(DashboardWidgetQuerySelectorModal));
//# sourceMappingURL=dashboardWidgetQuerySelectorModal.jsx.map