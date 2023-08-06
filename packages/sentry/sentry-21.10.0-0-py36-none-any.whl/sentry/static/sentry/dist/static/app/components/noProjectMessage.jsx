Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
/* TODO: replace with I/O when finished */
const hair_on_fire_svg_1 = (0, tslib_1.__importDefault)(require("sentry-images/spot/hair-on-fire.svg"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
function NoProjectMessage({ children, organization, projects, loadingProjects, superuserNeedsToBeProjectMember, }) {
    const orgSlug = organization.slug;
    const canCreateProject = organization.access.includes('project:write');
    const canJoinTeam = organization.access.includes('team:read');
    const { isSuperuser } = configStore_1.default.get('user');
    const orgHasProjects = !!(projects === null || projects === void 0 ? void 0 : projects.length);
    const hasProjectAccess = isSuperuser && !superuserNeedsToBeProjectMember
        ? !!(projects === null || projects === void 0 ? void 0 : projects.some(p => p.hasAccess))
        : !!(projects === null || projects === void 0 ? void 0 : projects.some(p => p.isMember && p.hasAccess));
    if (hasProjectAccess || loadingProjects) {
        return <react_1.Fragment>{children}</react_1.Fragment>;
    }
    // If the organization has some projects, but the user doesn't have access to
    // those projects, the primary action is to Join a Team. Otherwise the primary
    // action is to create a project.
    const joinTeamAction = (<button_1.default title={canJoinTeam ? undefined : (0, locale_1.t)('You do not have permission to join a team.')} disabled={!canJoinTeam} priority={orgHasProjects ? 'primary' : 'default'} to={`/settings/${orgSlug}/teams/`}>
      {(0, locale_1.t)('Join a Team')}
    </button_1.default>);
    const createProjectAction = (<button_1.default title={canCreateProject
            ? undefined
            : (0, locale_1.t)('You do not have permission to create a project.')} disabled={!canCreateProject} priority={orgHasProjects ? 'default' : 'primary'} to={`/organizations/${orgSlug}/projects/new/`}>
      {(0, locale_1.t)('Create project')}
    </button_1.default>);
    return (<Wrapper>
      <HeightWrapper>
        <hair_on_fire_svg_1.default src={hair_on_fire_svg_1.default} height={350} alt={(0, locale_1.t)('Nothing to see')}/>
        <Content>
          <StyledPageHeading>{(0, locale_1.t)('Remain Calm')}</StyledPageHeading>
          <HelpMessage>{(0, locale_1.t)('You need at least one project to use this view')}</HelpMessage>
          <Actions gap={1}>
            {!orgHasProjects ? (createProjectAction) : (<react_1.Fragment>
                {joinTeamAction}
                {createProjectAction}
              </react_1.Fragment>)}
          </Actions>
        </Content>
      </HeightWrapper>
    </Wrapper>);
}
const StyledPageHeading = (0, styled_1.default)(pageHeading_1.default) `
  font-size: 28px;
  margin-bottom: ${(0, space_1.default)(1.5)};
`;
const HelpMessage = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
`;
const Flex = (0, styled_1.default)('div') `
  display: flex;
`;
const Wrapper = (0, styled_1.default)(Flex) `
  flex: 1;
  align-items: center;
  justify-content: center;
`;
const HeightWrapper = (0, styled_1.default)(Flex) `
  height: 350px;
`;
const Content = (0, styled_1.default)(Flex) `
  flex-direction: column;
  justify-content: center;
  margin-left: 40px;
`;
const Actions = (0, styled_1.default)(buttonBar_1.default) `
  width: fit-content;
`;
exports.default = (0, withProjects_1.default)(NoProjectMessage);
//# sourceMappingURL=noProjectMessage.jsx.map