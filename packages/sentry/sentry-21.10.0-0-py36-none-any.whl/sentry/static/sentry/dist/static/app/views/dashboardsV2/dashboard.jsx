Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const core_1 = require("@dnd-kit/core");
const sortable_1 = require("@dnd-kit/sortable");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dashboards_1 = require("app/actionCreators/dashboards");
const indicator_1 = require("app/actionCreators/indicator");
const modal_1 = require("app/actionCreators/modal");
const tags_1 = require("app/actionCreators/tags");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const utils_1 = require("./widget/utils");
const addWidget_1 = (0, tslib_1.__importStar)(require("./addWidget"));
const sortableWidget_1 = (0, tslib_1.__importDefault)(require("./sortableWidget"));
const types_1 = require("./types");
class Dashboard extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleStartAdd = () => {
            const { organization, dashboard, selection } = this.props;
            (0, modal_1.openAddDashboardWidgetModal)({
                organization,
                dashboard,
                selection,
                onAddWidget: this.handleAddComplete,
            });
        };
        this.handleOpenWidgetBuilder = () => {
            const { router, paramDashboardId, organization, location } = this.props;
            if (paramDashboardId) {
                router.push({
                    pathname: `/organizations/${organization.slug}/dashboard/${paramDashboardId}/widget/new/`,
                    query: Object.assign(Object.assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                });
                return;
            }
            router.push({
                pathname: `/organizations/${organization.slug}/dashboards/new/widget/new/`,
                query: Object.assign(Object.assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
            });
        };
        this.handleAddComplete = (widget) => {
            this.props.onUpdate([...this.props.dashboard.widgets, widget]);
        };
        this.handleUpdateComplete = (index) => (nextWidget) => {
            const nextList = [...this.props.dashboard.widgets];
            nextList[index] = nextWidget;
            this.props.onUpdate(nextList);
        };
        this.handleDeleteWidget = (index) => () => {
            const nextList = [...this.props.dashboard.widgets];
            nextList.splice(index, 1);
            this.props.onUpdate(nextList);
        };
        this.handleEditWidget = (widget, index) => () => {
            const { organization, dashboard, selection, router, location, paramDashboardId, onSetWidgetToBeUpdated, } = this.props;
            if (organization.features.includes('metrics')) {
                onSetWidgetToBeUpdated(widget);
                if (paramDashboardId) {
                    router.push({
                        pathname: `/organizations/${organization.slug}/dashboard/${paramDashboardId}/widget/${index}/edit/`,
                        query: Object.assign(Object.assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                    });
                    return;
                }
                router.push({
                    pathname: `/organizations/${organization.slug}/dashboards/new/widget/${index}/edit/`,
                    query: Object.assign(Object.assign({}, location.query), { dataSet: utils_1.DataSet.EVENTS }),
                });
            }
            (0, modal_1.openAddDashboardWidgetModal)({
                organization,
                dashboard,
                widget,
                selection,
                onAddWidget: this.handleAddComplete,
                onUpdateWidget: this.handleUpdateComplete(index),
            });
        };
    }
    componentDidMount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { isEditing } = this.props;
            // Load organization tags when in edit mode.
            if (isEditing) {
                this.fetchTags();
            }
            this.addNewWidget();
        });
    }
    componentDidUpdate(prevProps) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { isEditing, newWidget } = this.props;
            // Load organization tags when going into edit mode.
            // We use tags on the add widget modal.
            if (prevProps.isEditing !== isEditing && isEditing) {
                this.fetchTags();
            }
            if (newWidget !== prevProps.newWidget) {
                this.addNewWidget();
            }
        });
    }
    addNewWidget() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, newWidget } = this.props;
            if (newWidget) {
                try {
                    yield (0, dashboards_1.validateWidget)(api, organization.slug, newWidget);
                    this.handleAddComplete(newWidget);
                }
                catch (error) {
                    // Don't do anything, widget isn't valid
                    (0, indicator_1.addErrorMessage)(error);
                }
            }
        });
    }
    fetchTags() {
        const { api, organization, selection } = this.props;
        (0, tags_1.loadOrganizationTags)(api, organization.slug, selection);
    }
    getWidgetIds() {
        return [
            ...this.props.dashboard.widgets.map((widget, index) => {
                return generateWidgetId(widget, index);
            }),
            addWidget_1.ADD_WIDGET_BUTTON_DRAG_ID,
        ];
    }
    renderWidget(widget, index) {
        const { isEditing } = this.props;
        const key = generateWidgetId(widget, index);
        const dragId = key;
        return (<sortableWidget_1.default key={key} widget={widget} dragId={dragId} isEditing={isEditing} onDelete={this.handleDeleteWidget(index)} onEdit={this.handleEditWidget(widget, index)}/>);
    }
    render() {
        const { isEditing, onUpdate, dashboard: { widgets }, organization, } = this.props;
        const items = this.getWidgetIds();
        return (<core_1.DndContext collisionDetection={core_1.closestCenter} onDragEnd={({ over, active }) => {
                const activeDragId = active.id;
                const getIndex = items.indexOf.bind(items);
                const activeIndex = activeDragId ? getIndex(activeDragId) : -1;
                if (over && over.id !== addWidget_1.ADD_WIDGET_BUTTON_DRAG_ID) {
                    const overIndex = getIndex(over.id);
                    if (activeIndex !== overIndex) {
                        onUpdate((0, sortable_1.arrayMove)(widgets, activeIndex, overIndex));
                    }
                }
            }}>
        <WidgetContainer>
          <sortable_1.SortableContext items={items} strategy={sortable_1.rectSortingStrategy}>
            {widgets.map((widget, index) => this.renderWidget(widget, index))}
            {isEditing && widgets.length < types_1.MAX_WIDGETS && (<addWidget_1.default orgFeatures={organization.features} onAddWidget={this.handleStartAdd} onOpenWidgetBuilder={this.handleOpenWidgetBuilder}/>)}
          </sortable_1.SortableContext>
        </WidgetContainer>
      </core_1.DndContext>);
    }
}
exports.default = (0, withApi_1.default)((0, withGlobalSelection_1.default)(Dashboard));
const WidgetContainer = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  grid-auto-flow: row dense;
  grid-gap: ${(0, space_1.default)(2)};

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    grid-template-columns: repeat(6, minmax(0, 1fr));
  }

  @media (min-width: ${p => p.theme.breakpoints[4]}) {
    grid-template-columns: repeat(8, minmax(0, 1fr));
  }
`;
function generateWidgetId(widget, index) {
    return widget.id ? `${widget.id}-index-${index}` : `index-${index}`;
}
//# sourceMappingURL=dashboard.jsx.map