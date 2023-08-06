Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamSelector = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const projects_1 = require("app/actionCreators/projects");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const selectControl_1 = (0, tslib_1.__importDefault)(require("app/components/forms/selectControl"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const useApi_1 = (0, tslib_1.__importDefault)(require("app/utils/useApi"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const UnassignedWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const StyledIconUser = (0, styled_1.default)(icons_1.IconUser) `
  margin-left: ${(0, space_1.default)(0.25)};
  margin-right: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray400};
`;
// An option to be unassigned on the team dropdown
const unassignedOption = {
    value: null,
    label: (<UnassignedWrapper>
      <StyledIconUser size="20px"/>
      {(0, locale_1.t)('Unassigned')}
    </UnassignedWrapper>),
    searchKey: 'unassigned',
    actor: null,
    disabled: false,
};
// Ensures that the svg icon is white when selected
const unassignedSelectStyles = {
    option: (provided, state) => (Object.assign(Object.assign({}, provided), { svg: {
            color: state.isSelected && state.theme.white,
        } })),
};
const placeholderSelectStyles = {
    input: (provided, state) => (Object.assign(Object.assign({}, provided), { display: 'grid', gridTemplateColumns: 'max-content 1fr', alignItems: 'center', gridGap: (0, space_1.default)(1), ':before': {
            backgroundColor: state.theme.backgroundSecondary,
            height: 24,
            width: 24,
            borderRadius: 3,
            content: '""',
            display: 'block',
        } })),
    placeholder: provided => (Object.assign(Object.assign({}, provided), { paddingLeft: 32 })),
};
function TeamSelector(props) {
    const { includeUnassigned, styles } = props, extraProps = (0, tslib_1.__rest)(props, ["includeUnassigned", "styles"]);
    const { teamFilter, organization, project, multiple, value, useId, onChange } = props;
    const api = (0, useApi_1.default)();
    const { teams, fetching, onSearch } = (0, useTeams_1.default)();
    // TODO(ts) This type could be improved when react-select types are better.
    const selectRef = (0, react_1.useRef)(null);
    const createTeamOption = (team) => ({
        value: useId ? team.id : team.slug,
        label: <idBadge_1.default team={team}/>,
        searchKey: `#${team.slug}`,
        actor: {
            type: 'team',
            id: team.id,
            name: team.slug,
        },
    });
    /**
     * Closes the select menu by blurring input if possible since that seems to
     * be the only way to close it.
     */
    function closeSelectMenu() {
        if (!selectRef.current) {
            return;
        }
        const select = selectRef.current.select;
        const input = select.inputRef;
        if (input) {
            // I don't think there's another way to close `react-select`
            input.blur();
        }
    }
    function handleAddTeamToProject(team) {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!project) {
                closeSelectMenu();
                return;
            }
            // Copy old value
            const oldValue = multiple ? [...(value !== null && value !== void 0 ? value : [])] : { value };
            // Optimistic update
            onChange === null || onChange === void 0 ? void 0 : onChange(createTeamOption(team));
            try {
                yield (0, projects_1.addTeamToProject)(api, organization.slug, project.slug, team);
            }
            catch (err) {
                // Unable to add team to project, revert select menu value
                onChange === null || onChange === void 0 ? void 0 : onChange(oldValue);
            }
            closeSelectMenu();
        });
    }
    function createTeamOutsideProjectOption(team) {
        // If the option/team is currently selected, optimistically assume it is now a part of the project
        if (value === (useId ? team.id : team.slug)) {
            return createTeamOption(team);
        }
        const canAddTeam = organization.access.includes('project:write');
        return Object.assign(Object.assign({}, createTeamOption(team)), { disabled: true, label: (<TeamOutsideProject>
          <DisabledLabel>
            <tooltip_1.default position="left" title={(0, locale_1.t)('%s is not a member of project', `#${team.slug}`)}>
              <idBadge_1.default team={team}/>
            </tooltip_1.default>
          </DisabledLabel>
          <tooltip_1.default title={canAddTeam
                    ? (0, locale_1.t)('Add %s to project', `#${team.slug}`)
                    : (0, locale_1.t)('You do not have permission to add team to project.')}>
            <AddToProjectButton type="button" size="zero" borderless disabled={!canAddTeam} onClick={() => handleAddTeamToProject(team)} icon={<icons_1.IconAdd isCircled/>}/>
          </tooltip_1.default>
        </TeamOutsideProject>) });
    }
    function getOptions() {
        const filteredTeams = teamFilter ? teams.filter(teamFilter) : teams;
        if (project) {
            const teamsInProjectIdSet = new Set(project.teams.map(team => team.id));
            const teamsInProject = filteredTeams.filter(team => teamsInProjectIdSet.has(team.id));
            const teamsNotInProject = filteredTeams.filter(team => !teamsInProjectIdSet.has(team.id));
            return [
                ...teamsInProject.map(createTeamOption),
                ...teamsNotInProject.map(createTeamOutsideProjectOption),
                ...(includeUnassigned ? [unassignedOption] : []),
            ];
        }
        return [
            ...filteredTeams.map(createTeamOption),
            ...(includeUnassigned ? [unassignedOption] : []),
        ];
    }
    return (<selectControl_1.default ref={selectRef} options={getOptions()} onInputChange={(0, debounce_1.default)(val => void onSearch(val), constants_1.DEFAULT_DEBOUNCE_DURATION)} isOptionDisabled={option => !!option.disabled} styles={Object.assign(Object.assign(Object.assign({}, (includeUnassigned ? unassignedSelectStyles : {})), placeholderSelectStyles), (styles !== null && styles !== void 0 ? styles : {}))} isLoading={fetching} {...extraProps}/>);
}
exports.TeamSelector = TeamSelector;
const TeamOutsideProject = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
`;
const DisabledLabel = (0, styled_1.default)('div') `
  display: flex;
  opacity: 0.5;
  overflow: hidden; /* Needed so that "Add to team" button can fit */
`;
const AddToProjectButton = (0, styled_1.default)(button_1.default) `
  flex-shrink: 0;
`;
// TODO(davidenwang): this is broken due to incorrect types on react-select
exports.default = (0, withOrganization_1.default)(TeamSelector);
//# sourceMappingURL=teamSelector.jsx.map