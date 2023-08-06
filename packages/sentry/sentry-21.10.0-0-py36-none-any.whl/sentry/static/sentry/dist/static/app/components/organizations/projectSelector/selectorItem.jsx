Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const featureDisabled_1 = (0, tslib_1.__importDefault)(require("app/components/acl/featureDisabled"));
const globalSelectionHeaderRow_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionHeaderRow"));
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const hovercard_1 = (0, tslib_1.__importDefault)(require("app/components/hovercard"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const bookmarkStar_1 = (0, tslib_1.__importDefault)(require("app/components/projects/bookmarkStar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const animations_1 = require("app/styles/animations");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const analytics_1 = require("app/utils/analytics");
const defaultProps = {
    multi: false,
    inputValue: '',
    isChecked: false,
};
class ProjectSelectorItem extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            bookmarkHasChanged: false,
        };
        this.handleClick = (event) => {
            const { project, onMultiSelect } = this.props;
            event.stopPropagation();
            if (onMultiSelect) {
                onMultiSelect(project, event);
            }
        };
        this.handleBookmarkToggle = (isBookmarked) => {
            const { organization } = this.props;
            (0, analytics_1.analytics)('projectselector.bookmark_toggle', {
                org_id: parseInt(organization.id, 10),
                bookmarked: isBookmarked,
            });
        };
        this.clearAnimation = () => {
            this.setState({ bookmarkHasChanged: false });
        };
    }
    componentDidUpdate(nextProps) {
        if (nextProps.project.isBookmarked !== this.props.project.isBookmarked) {
            this.setBookmarkHasChanged();
        }
    }
    setBookmarkHasChanged() {
        this.setState({ bookmarkHasChanged: true });
    }
    renderDisabledCheckbox({ children, features, }) {
        return (<hovercard_1.default body={<featureDisabled_1.default features={features} hideHelpToggle message={(0, locale_1.t)('Multiple project selection disabled')} featureName={(0, locale_1.t)('Multiple Project Selection')}/>}>
        {children}
      </hovercard_1.default>);
    }
    render() {
        const { project, multi, inputValue, isChecked, organization } = this.props;
        const { bookmarkHasChanged } = this.state;
        return (<BadgeAndActionsWrapper bookmarkHasChanged={bookmarkHasChanged} onAnimationEnd={this.clearAnimation}>
        <globalSelectionHeaderRow_1.default checked={isChecked} onCheckClick={this.handleClick} multi={multi} renderCheckbox={({ checkbox }) => (<feature_1.default features={['organizations:global-views']} hookName="feature-disabled:project-selector-checkbox" renderDisabled={this.renderDisabledCheckbox}>
              {checkbox}
            </feature_1.default>)}>
          <BadgeWrapper isMulti={multi}>
            <idBadge_1.default project={project} avatarSize={16} displayName={<highlight_1.default text={inputValue}>{project.slug}</highlight_1.default>} avatarProps={{ consistentWidth: true }} disableLink/>
          </BadgeWrapper>
          <StyledBookmarkStar project={project} organization={organization} bookmarkHasChanged={bookmarkHasChanged} onToggle={this.handleBookmarkToggle}/>
          <StyledLink to={`/organizations/${organization.slug}/projects/${project.slug}/?project=${project.id}`} onClick={e => e.stopPropagation()}>
            <icons_1.IconOpen />
          </StyledLink>

          <StyledLink to={`/settings/${organization.slug}/${project.slug}/`} onClick={e => e.stopPropagation()}>
            <icons_1.IconSettings />
          </StyledLink>
        </globalSelectionHeaderRow_1.default>
      </BadgeAndActionsWrapper>);
    }
}
ProjectSelectorItem.defaultProps = defaultProps;
exports.default = ProjectSelectorItem;
const StyledBookmarkStar = (0, styled_1.default)(bookmarkStar_1.default) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(0.5)};
  box-sizing: content-box;
  opacity: ${p => (p.project.isBookmarked ? 1 : 0.33)};
  transition: 0.5s opacity ease-out;
  display: block;
  width: 14px;
  height: 14px;
  margin-top: -${(0, space_1.default)(0.25)}; /* trivial alignment bump */
  ${p => p.bookmarkHasChanged &&
    (0, react_1.css) `
      animation: 0.5s ${(0, animations_1.pulse)(1.4)};
    `};
`;
const BadgeWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;
  ${p => !p.isMulti && 'flex: 1'};
  white-space: nowrap;
  overflow: hidden;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  color: ${p => p.theme.gray300};
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(0.25)} ${(0, space_1.default)(1)} ${(0, space_1.default)(1)};
  opacity: 0.33;
  transition: 0.5s opacity ease-out;
  :hover {
    color: ${p => p.theme.textColor};
  }
`;
const BadgeAndActionsWrapper = (0, styled_1.default)('div') `
  ${p => p.bookmarkHasChanged &&
    (0, react_1.css) `
      animation: 1s ${(0, animations_1.alertHighlight)('info', p.theme)};
    `};
  z-index: ${p => (p.bookmarkHasChanged ? 1 : 'inherit')};
  position: relative;
  border-style: solid;
  border-width: 1px 0;
  border-color: transparent;
  :hover {
    ${StyledBookmarkStar} {
      opacity: 1;
    }
    ${StyledLink} {
      opacity: 1;
    }
  }
`;
//# sourceMappingURL=selectorItem.jsx.map