Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const bookmarkStar_1 = (0, tslib_1.__importDefault)(require("app/components/projects/bookmarkStar"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
class ProjectItem extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isBookmarked: this.props.project.isBookmarked,
        };
        this.handleToggleBookmark = (isBookmarked) => {
            this.setState({ isBookmarked });
        };
    }
    render() {
        const { project, organization } = this.props;
        return (<Wrapper>
        <BookmarkLink organization={organization} project={project} isBookmarked={this.state.isBookmarked} onToggle={this.handleToggleBookmark}/>
        <projectBadge_1.default to={`/settings/${organization.slug}/projects/${project.slug}/`} avatarSize={18} project={project}/>
      </Wrapper>);
    }
}
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const BookmarkLink = (0, styled_1.default)(bookmarkStar_1.default) `
  margin-right: ${(0, space_1.default)(1)};
  margin-top: -${(0, space_1.default)(0.25)};
`;
exports.default = ProjectItem;
//# sourceMappingURL=settingsProjectItem.jsx.map