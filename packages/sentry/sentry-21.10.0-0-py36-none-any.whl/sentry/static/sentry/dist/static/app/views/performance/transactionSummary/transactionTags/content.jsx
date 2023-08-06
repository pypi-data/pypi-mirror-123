Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const styles_1 = require("app/components/charts/styles");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/searchBar"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const radio_1 = (0, tslib_1.__importDefault)(require("app/components/radio"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const segmentExplorerQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
const queryString_1 = require("app/utils/queryString");
const utils_1 = require("app/views/performance/transactionSummary/utils");
const filter_1 = require("../filter");
const tagExplorer_1 = require("../transactionOverview/tagExplorer");
const tagsDisplay_1 = (0, tslib_1.__importDefault)(require("./tagsDisplay"));
const utils_2 = require("./utils");
const TagsPageContent = (props) => {
    const { eventView, location, organization, projects } = props;
    const aggregateColumn = (0, tagExplorer_1.getTransactionField)(filter_1.SpanOperationBreakdownFilter.None, projects, eventView);
    return (<Layout.Main fullWidth>
      <segmentExplorerQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={20} sort="-sumdelta" allTagKeys>
        {({ isLoading, tableData }) => {
            return <InnerContent {...props} isLoading={isLoading} tableData={tableData}/>;
        }}
      </segmentExplorerQuery_1.default>
    </Layout.Main>);
};
function getTagKeyOptions(tableData) {
    const suspectTags = [];
    const otherTags = [];
    tableData.data.forEach(row => {
        const tagArray = row.comparison > 1 ? suspectTags : otherTags;
        tagArray.push(row.tags_key);
    });
    return {
        suspectTags,
        otherTags,
    };
}
const InnerContent = (props) => {
    const { eventView: _eventView, location, organization, tableData, isLoading } = props;
    const eventView = _eventView.clone();
    const tagOptions = tableData ? getTagKeyOptions(tableData) : null;
    const suspectTags = tagOptions ? tagOptions.suspectTags : [];
    const otherTags = tagOptions ? tagOptions.otherTags : [];
    const decodedTagKey = (0, utils_2.decodeSelectedTagKey)(location);
    const allTags = [...suspectTags, ...otherTags];
    const decodedTagFromOptions = decodedTagKey
        ? allTags.find(tag => tag === decodedTagKey)
        : undefined;
    const defaultTag = allTags.length ? allTags[0] : undefined;
    const initialTag = decodedTagFromOptions !== null && decodedTagFromOptions !== void 0 ? decodedTagFromOptions : defaultTag;
    const [tagSelected, _changeTagSelected] = (0, react_1.useState)(initialTag);
    const changeTagSelected = (tagKey) => {
        const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { tagKey }));
        react_router_1.browserHistory.replace({
            pathname: location.pathname,
            query: queryParams,
        });
        _changeTagSelected(tagKey);
    };
    (0, react_1.useEffect)(() => {
        if (initialTag) {
            changeTagSelected(initialTag);
        }
    }, [initialTag]);
    const handleSearch = (query) => {
        const queryParams = (0, getParams_1.getParams)(Object.assign(Object.assign({}, (location.query || {})), { query }));
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: queryParams,
        });
    };
    const changeTag = (tag) => {
        return changeTagSelected(tag);
    };
    if (tagSelected) {
        eventView.additionalConditions.setFilterValues('has', [tagSelected]);
    }
    const query = (0, queryString_1.decodeScalar)(location.query.query, '');
    return (<ReversedLayoutBody>
      <TagsSideBar suspectTags={suspectTags} otherTags={otherTags} tagSelected={tagSelected} changeTag={changeTag} isLoading={isLoading}/>
      <StyledMain>
        <StyledActions>
          <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
        </StyledActions>
        <tagsDisplay_1.default {...props} tagKey={tagSelected}/>
      </StyledMain>
    </ReversedLayoutBody>);
};
const TagsSideBar = (props) => {
    const { suspectTags, otherTags, changeTag, tagSelected, isLoading } = props;
    return (<StyledSide>
      <StyledSectionHeading>
        {(0, locale_1.t)('Suspect Tags')}
        <questionTooltip_1.default position="top" title={(0, locale_1.t)('Suspect tags are tags that often correspond to slower transaction')} size="sm"/>
      </StyledSectionHeading>
      {isLoading ? (<Center>
          <loadingIndicator_1.default mini/>
        </Center>) : suspectTags.length ? (suspectTags.map(tag => (<RadioLabel key={tag}>
            <radio_1.default aria-label={tag} checked={tagSelected === tag} onChange={() => changeTag(tag)}/>
            <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
          </RadioLabel>))) : (<div>{(0, locale_1.t)('No tags detected.')}</div>)}

      <utils_1.SidebarSpacer />
      <StyledSectionHeading>
        {(0, locale_1.t)('Other Tags')}
        <questionTooltip_1.default position="top" title={(0, locale_1.t)('Other common tags for this transaction')} size="sm"/>
      </StyledSectionHeading>

      {isLoading ? (<Center>
          <loadingIndicator_1.default mini/>
        </Center>) : otherTags.length ? (otherTags.map(tag => (<RadioLabel key={tag}>
            <radio_1.default aria-label={tag} checked={tagSelected === tag} onChange={() => changeTag(tag)}/>
            <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
          </RadioLabel>))) : (<div>{(0, locale_1.t)('No tags detected.')}</div>)}
    </StyledSide>);
};
const Center = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: center;
`;
const RadioLabel = (0, styled_1.default)('label') `
  cursor: pointer;
  margin-bottom: ${(0, space_1.default)(1)};
  font-weight: normal;
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content 1fr;
  align-items: center;
  grid-gap: ${(0, space_1.default)(1)};
`;
const SidebarTagValue = (0, styled_1.default)('span') `
  width: 100%;
`;
const StyledSectionHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  margin-bottom: ${(0, space_1.default)(2)};
`;
// TODO(k-fish): Adjust thirds layout to allow for this instead.
const ReversedLayoutBody = (0, styled_1.default)('div') `
  margin: 0;
  background-color: ${p => p.theme.background};
  flex-grow: 1;

  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    display: grid;
    grid-template-columns: auto 66%;
    align-content: start;
    grid-gap: ${(0, space_1.default)(3)};
  }

  @media (min-width: ${p => p.theme.breakpoints[2]}) {
    grid-template-columns: 225px minmax(100px, auto);
  }
`;
const StyledSide = (0, styled_1.default)('div') `
  grid-column: 1/2;
`;
const StyledMain = (0, styled_1.default)('div') `
  grid-column: 2/4;
  max-width: 100%;
`;
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  flex-grow: 1;
`;
const StyledActions = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
exports.default = TagsPageContent;
//# sourceMappingURL=content.jsx.map