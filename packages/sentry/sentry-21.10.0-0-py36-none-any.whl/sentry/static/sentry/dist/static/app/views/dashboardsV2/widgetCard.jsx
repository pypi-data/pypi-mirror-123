Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const modal_1 = require("app/actionCreators/modal");
const styles_1 = require("app/components/charts/styles");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const trackAdvancedAnalyticsEvent_1 = (0, tslib_1.__importDefault)(require("app/utils/analytics/trackAdvancedAnalyticsEvent"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const utils_2 = require("app/views/dashboardsV2/utils");
const contextMenu_1 = (0, tslib_1.__importDefault)(require("./contextMenu"));
const widgetCardChart_1 = (0, tslib_1.__importDefault)(require("./widgetCardChart"));
const widgetQueries_1 = (0, tslib_1.__importDefault)(require("./widgetQueries"));
class WidgetCard extends React.Component {
    shouldComponentUpdate(nextProps) {
        if (!(0, isEqual_1.default)(nextProps.widget, this.props.widget) ||
            !(0, utils_1.isSelectionEqual)(nextProps.selection, this.props.selection) ||
            this.props.isEditing !== nextProps.isEditing ||
            this.props.isSorting !== nextProps.isSorting ||
            this.props.hideToolbar !== nextProps.hideToolbar) {
            return true;
        }
        return false;
    }
    isAllowWidgetsToDiscover() {
        const { organization } = this.props;
        return organization.features.includes('connect-discover-and-dashboards');
    }
    renderToolbar() {
        const { onEdit, onDelete, draggableProps, hideToolbar, isEditing } = this.props;
        if (!isEditing) {
            return null;
        }
        return (<ToolbarPanel>
        <IconContainer style={{ visibility: hideToolbar ? 'hidden' : 'visible' }}>
          <IconClick>
            <StyledIconGrabbable color="textColor" {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.listeners} {...draggableProps === null || draggableProps === void 0 ? void 0 : draggableProps.attributes}/>
          </IconClick>
          <IconClick data-test-id="widget-edit" onClick={() => {
                onEdit();
            }}>
            <icons_1.IconEdit color="textColor"/>
          </IconClick>
          <IconClick data-test-id="widget-delete" onClick={() => {
                onDelete();
            }}>
            <icons_1.IconDelete color="textColor"/>
          </IconClick>
        </IconContainer>
      </ToolbarPanel>);
    }
    renderContextMenu() {
        const { widget, selection, organization, showContextMenu } = this.props;
        if (!showContextMenu) {
            return null;
        }
        const menuOptions = [];
        if ((widget.displayType === 'table' || this.isAllowWidgetsToDiscover()) &&
            organization.features.includes('discover-basic')) {
            // Open table widget in Discover
            if (widget.queries.length) {
                menuOptions.push(<menuItem_1.default key="open-discover" onClick={event => {
                        event.preventDefault();
                        (0, analytics_1.trackAnalyticsEvent)({
                            eventKey: 'dashboards2.tablewidget.open_in_discover',
                            eventName: 'Dashboards2: Table Widget - Open in Discover',
                            organization_id: parseInt(this.props.organization.id, 10),
                        });
                        if (widget.queries.length === 1) {
                            const eventView = (0, utils_2.eventViewFromWidget)(widget.title, widget.queries[0], selection, widget.displayType);
                            const discoverLocation = eventView.getResultsViewUrlTarget(organization.slug);
                            if (this.isAllowWidgetsToDiscover()) {
                                // Pull a max of 3 valid Y-Axis from the widget
                                const yAxisOptions = eventView
                                    .getYAxisOptions()
                                    .map(({ value }) => value);
                                discoverLocation.query.yAxis = widget.queries[0].fields
                                    .filter(field => yAxisOptions.includes(field))
                                    .slice(0, 3);
                            }
                            react_router_1.browserHistory.push(discoverLocation);
                        }
                        else {
                            (0, trackAdvancedAnalyticsEvent_1.default)('dashboards_views.query_selector.opened', {
                                organization,
                                widget_type: widget.displayType,
                            });
                            (0, modal_1.openDashboardWidgetQuerySelectorModal)({ organization, widget });
                        }
                    }}>
            {(0, locale_1.t)('Open in Discover')}
          </menuItem_1.default>);
            }
        }
        if (!menuOptions.length) {
            return null;
        }
        return (<ContextWrapper>
        <contextMenu_1.default>{menuOptions}</contextMenu_1.default>
      </ContextWrapper>);
    }
    render() {
        const { widget, api, organization, selection, renderErrorMessage, location, router } = this.props;
        return (<errorBoundary_1.default customComponent={<ErrorCard>{(0, locale_1.t)('Error loading widget data')}</ErrorCard>}>
        <StyledPanel isDragging={false}>
          <WidgetHeader>
            <WidgetTitle>{widget.title}</WidgetTitle>
            {this.renderContextMenu()}
          </WidgetHeader>
          <react_lazyload_1.default once height={200}>
            <widgetQueries_1.default api={api} organization={organization} widget={widget} selection={selection}>
              {({ tableResults, timeseriesResults, errorMessage, loading }) => {
                return (<React.Fragment>
                    {typeof renderErrorMessage === 'function'
                        ? renderErrorMessage(errorMessage)
                        : null}
                    <widgetCardChart_1.default timeseriesResults={timeseriesResults} tableResults={tableResults} errorMessage={errorMessage} loading={loading} location={location} widget={widget} selection={selection} router={router} organization={organization}/>
                    {this.renderToolbar()}
                  </React.Fragment>);
            }}
            </widgetQueries_1.default>
          </react_lazyload_1.default>
        </StyledPanel>
      </errorBoundary_1.default>);
    }
}
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withGlobalSelection_1.default)((0, react_router_1.withRouter)(WidgetCard))));
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
const StyledPanel = (0, styled_1.default)(panels_1.Panel, {
    shouldForwardProp: prop => prop !== 'isDragging',
}) `
  margin: 0;
  visibility: ${p => (p.isDragging ? 'hidden' : 'visible')};
  /* If a panel overflows due to a long title stretch its grid sibling */
  height: 100%;
  min-height: 96px;
`;
const ToolbarPanel = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  left: 0;
  z-index: 1;

  width: 100%;
  height: 100%;

  display: flex;
  justify-content: flex-end;
  align-items: flex-start;

  background-color: ${p => p.theme.overlayBackgroundAlpha};
  border-radius: ${p => p.theme.borderRadius};
`;
const IconContainer = (0, styled_1.default)('div') `
  display: flex;
  margin: 10px ${(0, space_1.default)(2)};
  touch-action: none;
`;
const IconClick = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(1)};

  &:hover {
    cursor: pointer;
  }
`;
const StyledIconGrabbable = (0, styled_1.default)(icons_1.IconGrabbable) `
  &:hover {
    cursor: grab;
  }
`;
const WidgetTitle = (0, styled_1.default)(styles_1.HeaderTitle) `
  ${overflowEllipsis_1.default};
`;
const WidgetHeader = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(3)} 0 ${(0, space_1.default)(3)};
  width: 100%;
  display: flex;
  justify-content: space-between;
`;
const ContextWrapper = (0, styled_1.default)('div') `
  margin-left: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=widgetCard.jsx.map