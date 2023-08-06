Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_select_1 = require("react-select");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const cloneDeep_1 = (0, tslib_1.__importDefault)(require("lodash/cloneDeep"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const pickProjectToContinue_1 = (0, tslib_1.__importDefault)(require("app/components/pickProjectToContinue"));
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const selectField_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/selectField"));
const buildStep_1 = (0, tslib_1.__importDefault)(require("../buildStep"));
const buildSteps_1 = (0, tslib_1.__importDefault)(require("../buildSteps"));
const choseDataStep_1 = (0, tslib_1.__importDefault)(require("../choseDataStep"));
const header_1 = (0, tslib_1.__importDefault)(require("../header"));
const utils_1 = require("../utils");
const card_1 = (0, tslib_1.__importDefault)(require("./card"));
const queries_1 = (0, tslib_1.__importDefault)(require("./queries"));
const searchQueryField_1 = (0, tslib_1.__importDefault)(require("./searchQueryField"));
class MetricWidget extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleFieldChange = (field, value) => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                if (field === 'displayType') {
                    if (state.title === (0, locale_1.t)('Custom %s Widget', state.displayType) ||
                        state.title === (0, locale_1.t)('Custom %s Widget', utils_1.DisplayType.AREA)) {
                        return Object.assign(Object.assign({}, newState), { title: (0, locale_1.t)('Custom %s Widget', utils_1.displayTypes[value]), widgetErrors: undefined });
                    }
                    (0, set_1.default)(newState, field, value);
                }
                return Object.assign(Object.assign({}, newState), { widgetErrors: undefined });
            });
        };
        this.handleRemoveQuery = (index) => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                newState.queries.splice(index, 1);
                return newState;
            });
        };
        this.handleAddQuery = () => {
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                newState.queries.push({});
                return newState;
            });
        };
        this.handleChangeQuery = (index, query) => {
            var _a, _b;
            const isMetricNew = ((_a = this.state.queries[index].metricMeta) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = query.metricMeta) === null || _b === void 0 ? void 0 : _b.name);
            if (isMetricNew) {
                query.aggregation = query.metricMeta ? query.metricMeta.operations[0] : undefined;
            }
            this.setState(state => {
                const newState = (0, cloneDeep_1.default)(state);
                (0, set_1.default)(newState, `queries.${index}`, query);
                return newState;
            });
        };
        this.handleProjectChange = (projectId) => {
            const { router, location } = this.props;
            // if we change project, we need to sync the project slug in the URL
            router.replace({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { project: projectId }),
            });
        };
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { title: (0, locale_1.t)('Custom %s Widget', utils_1.displayTypes[utils_1.DisplayType.AREA]), displayType: utils_1.DisplayType.AREA, metricMetas: [], metricTags: [], queries: [{}] });
    }
    get project() {
        const { projects, location } = this.props;
        const { query } = location;
        const { project: projectId } = query;
        return projects.find(project => project.id === projectId);
    }
    getEndpoints() {
        const { organization, loadingProjects } = this.props;
        if (this.isProjectMissingInUrl() || loadingProjects || !this.project) {
            return [];
        }
        const orgSlug = organization.slug;
        const projectSlug = this.project.slug;
        return [
            ['metricMetas', `/projects/${orgSlug}/${projectSlug}/metrics/meta/`],
            ['metricTags', `/projects/${orgSlug}/${projectSlug}/metrics/tags/`],
        ];
    }
    componentDidUpdate(prevProps, prevState) {
        var _a, _b;
        if (prevProps.loadingProjects && !this.props.loadingProjects) {
            this.reloadData();
        }
        if (!((_a = prevState.metricMetas) === null || _a === void 0 ? void 0 : _a.length) && !!((_b = this.state.metricMetas) === null || _b === void 0 ? void 0 : _b.length)) {
            this.handleChangeQuery(0, { metricMeta: this.state.metricMetas[0] });
        }
        super.componentDidUpdate(prevProps, prevState);
    }
    isProjectMissingInUrl() {
        const projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    }
    renderBody() {
        const { organization, router, projects, onChangeDataSet, selection, location, loadingProjects, goBackLocation, dashboardTitle, } = this.props;
        const { title, metricTags, searchQuery, metricMetas, queries, displayType } = this.state;
        const orgSlug = organization.slug;
        if (loadingProjects) {
            return this.renderLoading();
        }
        const selectedProject = this.project;
        if (this.isProjectMissingInUrl() || !selectedProject) {
            return (<pickProjectToContinue_1.default router={router} projects={projects.map(project => ({ id: project.id, slug: project.slug }))} nextPath={{
                    pathname: location.pathname,
                    query: location.query,
                }} noProjectRedirectPath={goBackLocation}/>);
        }
        if (!metricTags || !metricMetas) {
            return null;
        }
        return (<StyledPageContent>
        <header_1.default orgSlug={orgSlug} title={title} dashboardTitle={dashboardTitle} goBackLocation={goBackLocation} onChangeTitle={newTitle => this.handleFieldChange('title', newTitle)}/>
        <Layout.Body>
          <buildSteps_1.default>
            <buildStep_1.default title={(0, locale_1.t)('Choose your visualization')} description={(0, locale_1.t)('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <StyledSelectField name="displayType" options={[utils_1.DisplayType.LINE, utils_1.DisplayType.BAR, utils_1.DisplayType.AREA].map(value => ({ value, label: utils_1.displayTypes[value] }))} value={displayType} onChange={value => {
                this.handleFieldChange('displayType', value);
            }} inline={false} flexibleControlStateSize stacked/>
                <card_1.default router={router} location={location} selection={selection} organization={organization} api={this.api} project={selectedProject} widget={{
                title,
                searchQuery,
                displayType,
                groupings: queries,
            }}/>
              </VisualizationWrapper>
            </buildStep_1.default>
            <choseDataStep_1.default value={utils_1.DataSet.METRICS} onChange={onChangeDataSet}/>
            <buildStep_1.default title={(0, locale_1.t)('Choose your project')} description={(0, locale_1.t)('You’ll need to select a project to set metrics on.')}>
              <StyledSelectField name="project" options={projects.map(project => ({ value: project, label: project.slug }))} onChange={project => this.handleProjectChange(project.id)} value={selectedProject} components={{
                Option: (_a) => {
                    var { label } = _a, optionProps = (0, tslib_1.__rest)(_a, ["label"]);
                    const { data } = optionProps;
                    return (<react_select_1.components.Option label={label} {...optionProps}>
                        <projectBadge_1.default project={data.value} avatarSize={18} disableLink/>
                      </react_select_1.components.Option>);
                },
                SingleValue: (_a) => {
                    var { data } = _a, props = (0, tslib_1.__rest)(_a, ["data"]);
                    return (<react_select_1.components.SingleValue data={data} {...props}>
                      <projectBadge_1.default project={data.value} avatarSize={18} disableLink/>
                    </react_select_1.components.SingleValue>);
                },
            }} styles={{
                control: provided => (Object.assign(Object.assign({}, provided), { boxShadow: 'none' })),
            }} allowClear={false} inline={false} flexibleControlStateSize stacked/>
            </buildStep_1.default>
            <buildStep_1.default title={(0, locale_1.t)('Begin your search')} description={(0, locale_1.t)('Select a tag to compare releases, session data, etc.')}>
              <searchQueryField_1.default api={this.api} tags={metricTags} orgSlug={orgSlug} projectSlug={selectedProject.slug} query={searchQuery} onSearch={newQuery => this.handleFieldChange('searchQuery', newQuery)} onBlur={newQuery => this.handleFieldChange('searchQuery', newQuery)}/>
            </buildStep_1.default>
            <buildStep_1.default title={(0, locale_1.t)('Add queries')} description={(0, locale_1.t)('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
              <queries_1.default metricMetas={metricMetas} metricTags={metricTags} queries={queries} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleChangeQuery}/>
            </buildStep_1.default>
          </buildSteps_1.default>
        </Layout.Body>
      </StyledPageContent>);
    }
}
exports.default = (0, react_1.withTheme)((0, withProjects_1.default)((0, withGlobalSelection_1.default)(MetricWidget)));
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const StyledSelectField = (0, styled_1.default)(selectField_1.default) `
  padding-right: 0;
`;
const VisualizationWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
`;
//# sourceMappingURL=index.jsx.map