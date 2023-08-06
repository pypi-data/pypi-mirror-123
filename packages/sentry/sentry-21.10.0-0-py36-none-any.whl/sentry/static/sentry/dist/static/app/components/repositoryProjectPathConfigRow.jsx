Object.defineProperty(exports, "__esModule", { value: true });
exports.ButtonColumn = exports.InputPathColumn = exports.OutputPathColumn = exports.NameRepoColumn = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class RepositoryProjectPathConfigRow extends react_1.Component {
    render() {
        const { pathConfig, project, onEdit, onDelete } = this.props;
        return (<access_1.default access={['org:integrations']}>
        {({ hasAccess }) => (<react_1.Fragment>
            <exports.NameRepoColumn>
              <ProjectRepoHolder>
                <RepoName>{pathConfig.repoName}</RepoName>
                <ProjectAndBranch>
                  <idBadge_1.default project={project} avatarSize={14} displayName={project.slug} avatarProps={{ consistentWidth: true }}/>
                  <BranchWrapper>&nbsp;|&nbsp;{pathConfig.defaultBranch}</BranchWrapper>
                </ProjectAndBranch>
              </ProjectRepoHolder>
            </exports.NameRepoColumn>
            <exports.OutputPathColumn>{pathConfig.sourceRoot}</exports.OutputPathColumn>
            <exports.InputPathColumn>{pathConfig.stackRoot}</exports.InputPathColumn>
            <exports.ButtonColumn>
              <tooltip_1.default title={(0, locale_1.t)('You must be an organization owner, manager or admin to edit or remove a code mapping.')} disabled={hasAccess}>
                <StyledButton size="small" icon={<icons_1.IconEdit size="sm"/>} label={(0, locale_1.t)('edit')} disabled={!hasAccess} onClick={() => onEdit(pathConfig)}/>
                <confirm_1.default disabled={!hasAccess} onConfirm={() => onDelete(pathConfig)} message={(0, locale_1.t)('Are you sure you want to remove this code mapping?')}>
                  <StyledButton size="small" icon={<icons_1.IconDelete size="sm"/>} label={(0, locale_1.t)('delete')} disabled={!hasAccess}/>
                </confirm_1.default>
              </tooltip_1.default>
            </exports.ButtonColumn>
          </react_1.Fragment>)}
      </access_1.default>);
    }
}
exports.default = RepositoryProjectPathConfigRow;
const ProjectRepoHolder = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const RepoName = (0, styled_1.default)(`span`) `
  padding-bottom: ${(0, space_1.default)(1)};
`;
const StyledButton = (0, styled_1.default)(button_1.default) `
  margin: ${(0, space_1.default)(0.5)};
`;
const ProjectAndBranch = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  color: ${p => p.theme.gray300};
`;
// match the line height of the badge
const BranchWrapper = (0, styled_1.default)('div') `
  line-height: 1.2;
`;
// Columns below
const Column = (0, styled_1.default)('span') `
  overflow: hidden;
  overflow-wrap: break-word;
`;
exports.NameRepoColumn = (0, styled_1.default)(Column) `
  grid-area: name-repo;
`;
exports.OutputPathColumn = (0, styled_1.default)(Column) `
  grid-area: output-path;
`;
exports.InputPathColumn = (0, styled_1.default)(Column) `
  grid-area: input-path;
`;
exports.ButtonColumn = (0, styled_1.default)(Column) `
  grid-area: button;
  text-align: right;
`;
//# sourceMappingURL=repositoryProjectPathConfigRow.jsx.map