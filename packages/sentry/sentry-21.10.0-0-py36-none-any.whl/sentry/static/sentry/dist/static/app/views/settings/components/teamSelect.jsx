Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const teamBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/teamBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const useTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/useTeams"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
function TeamSelect({ disabled, selectedTeams, menuHeader, organization, onAddTeam, onRemoveTeam, confirmLastTeamRemoveMessage, loadingTeams, }) {
    const { teams, onSearch, fetching } = (0, useTeams_1.default)();
    const handleAddTeam = (option) => {
        const team = teams.find(tm => tm.slug === option.value);
        if (team) {
            onAddTeam(team);
        }
    };
    const renderBody = () => {
        if (selectedTeams.length === 0) {
            return <emptyMessage_1.default>{(0, locale_1.t)('No Teams assigned')}</emptyMessage_1.default>;
        }
        const confirmMessage = selectedTeams.length === 1 && confirmLastTeamRemoveMessage
            ? confirmLastTeamRemoveMessage
            : null;
        return selectedTeams.map(team => (<TeamRow key={team.slug} orgId={organization.slug} team={team} onRemove={slug => onRemoveTeam(slug)} disabled={disabled} confirmMessage={confirmMessage}/>));
    };
    // Only show options that aren't selected in the dropdown
    const options = teams
        .filter(team => !selectedTeams.some(selectedTeam => selectedTeam.slug === team.slug))
        .map((team, index) => ({
        index,
        value: team.slug,
        searchKey: team.slug,
        label: <DropdownTeamBadge avatarSize={18} team={team}/>,
    }));
    return (<panels_1.Panel>
      <panels_1.PanelHeader hasButtons>
        {(0, locale_1.t)('Team')}
        <dropdownAutoComplete_1.default items={options} busyItemsStillVisible={fetching} onChange={(0, debounce_1.default)(e => onSearch(e.target.value), constants_1.DEFAULT_DEBOUNCE_DURATION)} onSelect={handleAddTeam} emptyMessage={(0, locale_1.t)('No teams')} menuHeader={menuHeader} disabled={disabled} alignMenu="right">
          {({ isOpen }) => (<dropdownButton_1.default aria-label={(0, locale_1.t)('Add Team')} isOpen={isOpen} size="xsmall" disabled={disabled}>
              {(0, locale_1.t)('Add Team')}
            </dropdownButton_1.default>)}
        </dropdownAutoComplete_1.default>
      </panels_1.PanelHeader>

      <panels_1.PanelBody>{loadingTeams ? <loadingIndicator_1.default /> : renderBody()}</panels_1.PanelBody>
    </panels_1.Panel>);
}
const TeamRow = ({ orgId, team, onRemove, disabled, confirmMessage }) => (<TeamPanelItem>
    <StyledLink to={`/settings/${orgId}/teams/${team.slug}/`}>
      <teamBadge_1.default team={team}/>
    </StyledLink>
    <confirm_1.default message={confirmMessage} bypass={!confirmMessage} onConfirm={() => onRemove(team.slug)} disabled={disabled}>
      <button_1.default size="xsmall" icon={<icons_1.IconSubtract isCircled size="xs"/>} disabled={disabled}>
        {(0, locale_1.t)('Remove')}
      </button_1.default>
    </confirm_1.default>
  </TeamPanelItem>);
const DropdownTeamBadge = (0, styled_1.default)(teamBadge_1.default) `
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  text-transform: none;
`;
const TeamPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: ${(0, space_1.default)(2)};
  align-items: center;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = TeamSelect;
//# sourceMappingURL=teamSelect.jsx.map