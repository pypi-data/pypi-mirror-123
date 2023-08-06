Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const locale_1 = require("app/locale");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const textBlock_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/text/textBlock"));
const allTeamsRow_1 = (0, tslib_1.__importDefault)(require("./allTeamsRow"));
function AllTeamsList({ organization, urlPrefix, openMembership, teamList, access, }) {
    const teamNodes = teamList.map(team => (<allTeamsRow_1.default urlPrefix={urlPrefix} team={team} organization={organization} openMembership={openMembership} key={team.slug}/>));
    if (!teamNodes.length) {
        const canCreateTeam = access.has('project:admin');
        return (<emptyMessage_1.default>
        {(0, locale_1.tct)('No teams here. [teamCreate]', {
                root: <textBlock_1.default noMargin/>,
                teamCreate: canCreateTeam
                    ? (0, locale_1.tct)('You can always [link:create one].', {
                        link: (<StyledButton priority="link" onClick={() => (0, modal_1.openCreateTeamModal)({
                                organization,
                            })}/>),
                    })
                    : null,
            })}
      </emptyMessage_1.default>);
    }
    return <react_1.Fragment>{teamNodes}</react_1.Fragment>;
}
exports.default = AllTeamsList;
const StyledButton = (0, styled_1.default)(button_1.default) `
  font-size: ${p => p.theme.fontSizeLarge};
`;
//# sourceMappingURL=allTeamsList.jsx.map