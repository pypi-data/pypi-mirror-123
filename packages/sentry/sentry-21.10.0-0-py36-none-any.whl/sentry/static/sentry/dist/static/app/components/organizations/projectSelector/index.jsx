Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const selectorItem_1 = (0, tslib_1.__importDefault)(require("./selectorItem"));
const ProjectSelector = (_a) => {
    var { children, organization, menuFooter, className, rootClassName, onClose, onFilterChange, onScroll, searching, paginated, multiProjects, onSelect, onMultiSelect, multi = false, selectedProjects = [] } = _a, props = (0, tslib_1.__rest)(_a, ["children", "organization", "menuFooter", "className", "rootClassName", "onClose", "onFilterChange", "onScroll", "searching", "paginated", "multiProjects", "onSelect", "onMultiSelect", "multi", "selectedProjects"]);
    const getProjects = () => {
        const { nonMemberProjects = [] } = props;
        return [
            (0, sortBy_1.default)(multiProjects, project => [
                !selectedProjects.find(selectedProject => selectedProject.slug === project.slug),
                !project.isBookmarked,
                project.slug,
            ]),
            (0, sortBy_1.default)(nonMemberProjects, project => [project.slug]),
        ];
    };
    const [projects, nonMemberProjects] = getProjects();
    const handleSelect = ({ value: project }) => {
        onSelect(project);
    };
    const handleMultiSelect = (project, event) => {
        if (!onMultiSelect) {
            // eslint-disable-next-line no-console
            console.error('ProjectSelector is a controlled component but `onMultiSelect` callback is not defined');
            return;
        }
        const selectedProjectsMap = new Map(selectedProjects.map(p => [p.slug, p]));
        if (selectedProjectsMap.has(project.slug)) {
            // unselected a project
            selectedProjectsMap.delete(project.slug);
            onMultiSelect(Array.from(selectedProjectsMap.values()), event);
            return;
        }
        selectedProjectsMap.set(project.slug, project);
        onMultiSelect(Array.from(selectedProjectsMap.values()), event);
    };
    const getProjectItem = (project) => ({
        value: project,
        searchKey: project.slug,
        label: ({ inputValue }) => (<selectorItem_1.default project={project} organization={organization} multi={multi} inputValue={inputValue} isChecked={!!selectedProjects.find(({ slug }) => slug === project.slug)} onMultiSelect={handleMultiSelect}/>),
    });
    const getItems = (hasProjects) => {
        if (!hasProjects) {
            return [];
        }
        return [
            {
                hideGroupLabel: true,
                items: projects.map(getProjectItem),
            },
            {
                hideGroupLabel: nonMemberProjects.length === 0,
                itemSize: 'small',
                id: 'no-membership-header',
                label: <Label>{(0, locale_1.t)("Projects I don't belong to")}</Label>,
                items: nonMemberProjects.map(getProjectItem),
            },
        ];
    };
    const hasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length) || !!(nonMemberProjects === null || nonMemberProjects === void 0 ? void 0 : nonMemberProjects.length);
    const newProjectUrl = `/organizations/${organization.slug}/projects/new/`;
    const hasProjectWrite = organization.access.includes('project:write');
    return (<dropdownAutoComplete_1.default blendCorner={false} searchPlaceholder={(0, locale_1.t)('Filter projects')} onSelect={handleSelect} onClose={onClose} onChange={onFilterChange} busyItemsStillVisible={searching} onScroll={onScroll} maxHeight={500} inputProps={{ style: { padding: 8, paddingLeft: 10 } }} rootClassName={rootClassName} className={className} emptyMessage={(0, locale_1.t)('You have no projects')} noResultsMessage={(0, locale_1.t)('No projects found')} virtualizedHeight={theme_1.default.headerSelectorRowHeight} virtualizedLabelHeight={theme_1.default.headerSelectorLabelHeight} emptyHidesInput={!paginated} inputActions={<AddButton disabled={!hasProjectWrite} to={newProjectUrl} size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} title={!hasProjectWrite ? (0, locale_1.t)("You don't have permission to add a project") : undefined}>
          {(0, locale_1.t)('Project')}
        </AddButton>} menuFooter={renderProps => {
            const renderedFooter = typeof menuFooter === 'function' ? menuFooter(renderProps) : menuFooter;
            const showCreateProjectButton = !hasProjects && hasProjectWrite;
            if (!renderedFooter && !showCreateProjectButton) {
                return null;
            }
            return (<React.Fragment>
            {showCreateProjectButton && (<CreateProjectButton priority="primary" size="small" to={newProjectUrl}>
                {(0, locale_1.t)('Create project')}
              </CreateProjectButton>)}
            {renderedFooter}
          </React.Fragment>);
        }} items={getItems(hasProjects)} allowActorToggle closeOnSelect>
      {renderProps => children(Object.assign(Object.assign({}, renderProps), { selectedProjects }))}
    </dropdownAutoComplete_1.default>);
};
exports.default = ProjectSelector;
const Label = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
`;
const AddButton = (0, styled_1.default)(button_1.default) `
  display: block;
  margin: 0 ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray300};
  :hover {
    color: ${p => p.theme.subText};
  }
`;
const CreateProjectButton = (0, styled_1.default)(button_1.default) `
  display: block;
  text-align: center;
  margin: ${(0, space_1.default)(0.5)} 0;
`;
//# sourceMappingURL=index.jsx.map