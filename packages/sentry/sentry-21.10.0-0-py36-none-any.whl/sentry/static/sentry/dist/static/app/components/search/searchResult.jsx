Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const icons_1 = require("app/icons");
const pluginIcon_1 = (0, tslib_1.__importDefault)(require("app/plugins/components/pluginIcon"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const highlightFuseMatches_1 = (0, tslib_1.__importDefault)(require("app/utils/highlightFuseMatches"));
class SearchResult extends react_1.Component {
    renderContent() {
        const { highlighted, item, matches, params } = this.props;
        const { sourceType, model, extra } = item;
        let { title, description } = item;
        if (matches) {
            // TODO(ts) Type this better.
            const HighlightedMarker = (p) => (<HighlightMarker highlighted={highlighted} {...p}/>);
            const matchedTitle = matches && matches.find(({ key }) => key === 'title');
            const matchedDescription = matches && matches.find(({ key }) => key === 'description');
            title = matchedTitle
                ? (0, highlightFuseMatches_1.default)(matchedTitle, HighlightedMarker)
                : title;
            description = matchedDescription
                ? (0, highlightFuseMatches_1.default)(matchedDescription, HighlightedMarker)
                : description;
        }
        if (['organization', 'member', 'project', 'team'].includes(sourceType)) {
            const DescriptionNode = (<BadgeDetail highlighted={highlighted}>{description}</BadgeDetail>);
            const badgeProps = {
                displayName: title,
                displayEmail: DescriptionNode,
                description: DescriptionNode,
                useLink: false,
                orgId: params.orgId,
                avatarSize: 32,
                [sourceType]: model,
            };
            return <idBadge_1.default {...badgeProps}/>;
        }
        return (<react_1.Fragment>
        <div>
          <SearchTitle>{title}</SearchTitle>
        </div>
        {description && <SearchDetail>{description}</SearchDetail>}
        {extra && <ExtraDetail>{extra}</ExtraDetail>}
      </react_1.Fragment>);
    }
    renderResultType() {
        const { item } = this.props;
        const { resultType, model } = item;
        const isSettings = resultType === 'settings';
        const isField = resultType === 'field';
        const isRoute = resultType === 'route';
        const isIntegration = resultType === 'integration';
        if (isSettings) {
            return <icons_1.IconSettings />;
        }
        if (isField) {
            return <icons_1.IconInput />;
        }
        if (isRoute) {
            return <icons_1.IconLink />;
        }
        if (isIntegration) {
            return <StyledPluginIcon pluginId={model.slug}/>;
        }
        return null;
    }
    render() {
        return (<Wrapper>
        <Content>{this.renderContent()}</Content>
        <div>{this.renderResultType()}</div>
      </Wrapper>);
    }
}
exports.default = (0, react_router_1.withRouter)(SearchResult);
// This is for tests
const SearchTitle = (0, styled_1.default)('span') ``;
const SearchDetail = (0, styled_1.default)('div') `
  font-size: 0.8em;
  line-height: 1.3;
  margin-top: 4px;
  opacity: 0.8;
`;
const ExtraDetail = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeSmall};
  color: ${p => p.theme.gray300};
  margin-top: ${(0, space_1.default)(0.5)};
`;
const BadgeDetail = (0, styled_1.default)('div') `
  line-height: 1.3;
  color: ${p => (p.highlighted ? p.theme.purple300 : null)};
`;
const Wrapper = (0, styled_1.default)('div') `
  display: flex;
  justify-content: space-between;
  align-items: center;
`;
const Content = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
`;
const StyledPluginIcon = (0, styled_1.default)(pluginIcon_1.default) `
  flex-shrink: 0;
`;
const HighlightMarker = (0, styled_1.default)('mark') `
  padding: 0;
  background: transparent;
  font-weight: bold;
  color: ${p => p.theme.active};
`;
//# sourceMappingURL=searchResult.jsx.map