Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const dataExport_1 = (0, tslib_1.__importStar)(require("app/components/dataExport"));
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const dropdownLink_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownLink"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const userBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/userBadge"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const DEFAULT_SORT = 'count';
class GroupTagValues extends asyncComponent_1.default {
    getEndpoints() {
        const { environments: environment } = this.props;
        const { groupId, tagKey } = this.props.params;
        return [
            ['tag', `/issues/${groupId}/tags/${tagKey}/`],
            [
                'tagValueList',
                `/issues/${groupId}/tags/${tagKey}/values/`,
                { query: { environment, sort: this.getSort() } },
            ],
        ];
    }
    getSort() {
        return this.props.location.query.sort || DEFAULT_SORT;
    }
    renderLoading() {
        return this.renderBody();
    }
    renderResults() {
        const { baseUrl, project, environments: environment, params: { orgId, groupId, tagKey }, } = this.props;
        const { tagValueList, tag } = this.state;
        const discoverFields = [
            'title',
            'release',
            'environment',
            'user.display',
            'timestamp',
        ];
        return tagValueList === null || tagValueList === void 0 ? void 0 : tagValueList.map((tagValue, tagValueIdx) => {
            var _a, _b;
            const pct = (tag === null || tag === void 0 ? void 0 : tag.totalValues)
                ? `${(0, utils_1.percent)(tagValue.count, tag === null || tag === void 0 ? void 0 : tag.totalValues).toFixed(2)}%`
                : '--';
            const key = (_a = tagValue.key) !== null && _a !== void 0 ? _a : tagKey;
            const issuesQuery = tagValue.query || `${key}:"${tagValue.value}"`;
            const discoverView = eventView_1.default.fromSavedQuery({
                id: undefined,
                name: key,
                fields: [key, ...discoverFields.filter(field => field !== key)],
                orderby: '-timestamp',
                query: `issue.id:${groupId} ${issuesQuery}`,
                projects: [Number(project === null || project === void 0 ? void 0 : project.id)],
                environment,
                version: 2,
                range: '90d',
            });
            const issuesPath = `/organizations/${orgId}/issues/`;
            return (<react_1.Fragment key={tagValueIdx}>
          <NameColumn>
            <NameWrapper data-test-id="group-tag-value">
              <globalSelectionLink_1.default to={{
                    pathname: `${baseUrl}events/`,
                    query: { query: issuesQuery },
                }}>
                {key === 'user' ? (<userBadge_1.default user={Object.assign(Object.assign({}, tagValue), { id: (_b = tagValue.identifier) !== null && _b !== void 0 ? _b : '' })} avatarSize={20} hideEmail/>) : (<deviceName_1.default value={tagValue.name}/>)}
              </globalSelectionLink_1.default>
            </NameWrapper>

            {tagValue.email && (<StyledExternalLink href={`mailto:${tagValue.email}`} data-test-id="group-tag-mail">
                <icons_1.IconMail size="xs" color="gray300"/>
              </StyledExternalLink>)}
            {(0, utils_1.isUrl)(tagValue.value) && (<StyledExternalLink href={tagValue.value} data-test-id="group-tag-url">
                <icons_1.IconOpen size="xs" color="gray300"/>
              </StyledExternalLink>)}
          </NameColumn>
          <RightAlignColumn>{pct}</RightAlignColumn>
          <RightAlignColumn>{tagValue.count.toLocaleString()}</RightAlignColumn>
          <RightAlignColumn>
            <timeSince_1.default date={tagValue.lastSeen}/>
          </RightAlignColumn>
          <RightAlignColumn>
            <dropdownLink_1.default anchorRight alwaysRenderMenu={false} caret={false} title={<button_1.default tooltipProps={{
                        containerDisplayMode: 'flex',
                    }} size="small" type="button" aria-label={(0, locale_1.t)('Show more')} icon={<icons_1.IconEllipsis size="xs"/>}/>}>
              <feature_1.default features={['organizations:discover-basic']}>
                <li>
                  <link_1.default to={discoverView.getResultsViewUrlTarget(orgId)}>
                    {(0, locale_1.t)('Open in Discover')}
                  </link_1.default>
                </li>
              </feature_1.default>
              <li>
                <globalSelectionLink_1.default to={{ pathname: issuesPath, query: { query: issuesQuery } }}>
                  {(0, locale_1.t)('Search All Issues with Tag Value')}
                </globalSelectionLink_1.default>
              </li>
            </dropdownLink_1.default>
          </RightAlignColumn>
        </react_1.Fragment>);
        });
    }
    renderBody() {
        const { group, params: { orgId, tagKey }, location: { query }, environments, } = this.props;
        const { tagValueList, tag, tagValueListPageLinks, loading } = this.state;
        const { cursor: _cursor, page: _page } = query, currentQuery = (0, tslib_1.__rest)(query, ["cursor", "page"]);
        const title = tagKey === 'user' ? (0, locale_1.t)('Affected Users') : tagKey;
        const sort = this.getSort();
        const sortArrow = <icons_1.IconArrow color="gray300" size="xs" direction="down"/>;
        const lastSeenColumnHeader = (<StyledSortLink to={{
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { sort: 'date' }),
            }}>
        {(0, locale_1.t)('Last Seen')} {sort === 'date' && sortArrow}
      </StyledSortLink>);
        const countColumnHeader = (<StyledSortLink to={{
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, currentQuery), { sort: 'count' }),
            }}>
        {(0, locale_1.t)('Count')} {sort === 'count' && sortArrow}
      </StyledSortLink>);
        return (<react_1.Fragment>
        <TitleWrapper>
          <Title>{(0, locale_1.t)('Tag Details')}</Title>
          <buttonBar_1.default gap={1}>
            <button_1.default size="small" priority="default" href={`/${orgId}/${group.project.slug}/issues/${group.id}/tags/${tagKey}/export/`}>
              {(0, locale_1.t)('Export Page to CSV')}
            </button_1.default>
            <dataExport_1.default payload={{
                queryType: dataExport_1.ExportQueryType.IssuesByTag,
                queryInfo: {
                    project: group.project.id,
                    group: group.id,
                    key: tagKey,
                },
            }}/>
          </buttonBar_1.default>
        </TitleWrapper>
        <StyledPanelTable isLoading={loading} isEmpty={(tagValueList === null || tagValueList === void 0 ? void 0 : tagValueList.length) === 0} headers={[
                title,
                <PercentColumnHeader key="percent">{(0, locale_1.t)('Percent')}</PercentColumnHeader>,
                countColumnHeader,
                lastSeenColumnHeader,
                '',
            ]} emptyMessage={(0, locale_1.t)('Sorry, the tags for this issue could not be found.')} emptyAction={!!(environments === null || environments === void 0 ? void 0 : environments.length)
                ? (0, locale_1.t)('No tags were found for the currently selected environments')
                : null}>
          {tagValueList && tag && this.renderResults()}
        </StyledPanelTable>
        <StyledPagination pageLinks={tagValueListPageLinks}/>
      </react_1.Fragment>);
    }
}
exports.default = GroupTagValues;
const TitleWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: row;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(2)};
`;
const Title = (0, styled_1.default)('h3') `
  margin: 0;
`;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  white-space: nowrap;
  font-size: ${p => p.theme.fontSizeMedium};

  overflow: auto;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    overflow: initial;
  }

  & > * {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  }
`;
const PercentColumnHeader = (0, styled_1.default)('div') `
  text-align: right;
`;
const StyledSortLink = (0, styled_1.default)(link_1.default) `
  text-align: right;
  color: inherit;

  :hover {
    color: inherit;
  }
`;
const StyledExternalLink = (0, styled_1.default)(externalLink_1.default) `
  margin-left: ${(0, space_1.default)(0.5)};
`;
const Column = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
`;
const NameColumn = (0, styled_1.default)(Column) `
  ${overflowEllipsis_1.default};
  display: flex;
  min-width: 320px;
`;
const NameWrapper = (0, styled_1.default)('span') `
  ${overflowEllipsis_1.default};
  width: auto;
`;
const RightAlignColumn = (0, styled_1.default)(Column) `
  justify-content: flex-end;
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin: 0;
`;
//# sourceMappingURL=groupTagValues.jsx.map