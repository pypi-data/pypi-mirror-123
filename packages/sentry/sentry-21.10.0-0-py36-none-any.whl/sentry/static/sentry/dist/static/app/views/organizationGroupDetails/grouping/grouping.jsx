Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const pagination_1 = (0, tslib_1.__importDefault)(require("app/components/pagination"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const parseLinkHeader_1 = (0, tslib_1.__importDefault)(require("app/utils/parseLinkHeader"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const rangeSlider_1 = (0, tslib_1.__importStar)(require("app/views/settings/components/forms/controls/rangeSlider"));
const errorMessage_1 = (0, tslib_1.__importDefault)(require("./errorMessage"));
const newIssue_1 = (0, tslib_1.__importDefault)(require("./newIssue"));
function LinkFooter() {
    return (<Footer>
      <externalLink_1.default href={`mailto:grouping@sentry.io?subject=${encodeURIComponent('Grouping Feedback')}&body=${encodeURIComponent(`URL: ${window.location.href}\n\nThanks for taking the time to provide us feedback. What's on your mind?`)}`}>
        <StyledIconMegaphone /> {(0, locale_1.t)('Give Feedback')}
      </externalLink_1.default>
    </Footer>);
}
function Grouping({ api, groupId, location, organization, router, projSlug }) {
    var _a, _b;
    const { cursor, level } = location.query;
    const [isLoading, setIsLoading] = (0, react_1.useState)(false);
    const [isGroupingLevelDetailsLoading, setIsGroupingLevelDetailsLoading] = (0, react_1.useState)(false);
    const [error, setError] = (0, react_1.useState)(undefined);
    const [groupingLevels, setGroupingLevels] = (0, react_1.useState)([]);
    const [activeGroupingLevel, setActiveGroupingLevel] = (0, react_1.useState)(undefined);
    const [activeGroupingLevelDetails, setActiveGroupingLevelDetails] = (0, react_1.useState)([]);
    const [pagination, setPagination] = (0, react_1.useState)('');
    (0, react_1.useEffect)(() => {
        fetchGroupingLevels();
        return react_router_1.browserHistory.listen(handleRouteLeave);
    }, []);
    (0, react_1.useEffect)(() => {
        setSecondGrouping();
    }, [groupingLevels]);
    (0, react_1.useEffect)(() => {
        updateUrlWithNewLevel();
    }, [activeGroupingLevel]);
    (0, react_1.useEffect)(() => {
        fetchGroupingLevelDetails();
    }, [activeGroupingLevel, cursor]);
    function handleRouteLeave(newLocation) {
        if (newLocation.pathname === location.pathname ||
            (newLocation.pathname !== location.pathname &&
                newLocation.query.cursor === undefined &&
                newLocation.query.level === undefined)) {
            return true;
        }
        // Removes cursor and level from the URL on route leave
        // so that the parameters will not interfere with other pages
        react_router_1.browserHistory.replace({
            pathname: newLocation.pathname,
            query: Object.assign(Object.assign({}, newLocation.query), { cursor: undefined, level: undefined }),
        });
        return false;
    }
    const handleSetActiveGroupingLevel = (0, debounce_1.default)((groupingLevelId) => {
        setActiveGroupingLevel(Number(groupingLevelId));
    }, constants_1.DEFAULT_DEBOUNCE_DURATION);
    function fetchGroupingLevels() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            setIsLoading(true);
            setError(undefined);
            try {
                const response = yield api.requestPromise(`/issues/${groupId}/grouping/levels/`);
                setIsLoading(false);
                setGroupingLevels(response.levels);
            }
            catch (err) {
                setIsLoading(false);
                setError(err);
            }
        });
    }
    function fetchGroupingLevelDetails() {
        var _a;
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            if (!groupingLevels.length || !(0, utils_1.defined)(activeGroupingLevel)) {
                return;
            }
            setIsGroupingLevelDetailsLoading(true);
            setError(undefined);
            try {
                const [data, , resp] = yield api.requestPromise(`/issues/${groupId}/grouping/levels/${activeGroupingLevel}/new-issues/`, {
                    method: 'GET',
                    includeAllArgs: true,
                    query: Object.assign(Object.assign({}, location.query), { per_page: 10 }),
                });
                const pageLinks = (_a = resp === null || resp === void 0 ? void 0 : resp.getResponseHeader) === null || _a === void 0 ? void 0 : _a.call(resp, 'Link');
                setPagination(pageLinks !== null && pageLinks !== void 0 ? pageLinks : '');
                setActiveGroupingLevelDetails(Array.isArray(data) ? data : [data]);
                setIsGroupingLevelDetailsLoading(false);
            }
            catch (err) {
                setIsGroupingLevelDetailsLoading(false);
                setError(err);
            }
        });
    }
    function updateUrlWithNewLevel() {
        if (!(0, utils_1.defined)(activeGroupingLevel) || level === activeGroupingLevel) {
            return;
        }
        router.replace({
            pathname: location.pathname,
            query: Object.assign(Object.assign({}, location.query), { cursor: undefined, level: activeGroupingLevel }),
        });
    }
    function setSecondGrouping() {
        if (!groupingLevels.length) {
            return;
        }
        if ((0, utils_1.defined)(level)) {
            if (!(0, utils_1.defined)(groupingLevels[level])) {
                setError((0, locale_1.t)('The level you were looking for was not found.'));
                return;
            }
            if (level === activeGroupingLevel) {
                return;
            }
            setActiveGroupingLevel(level);
            return;
        }
        if (groupingLevels.length > 1) {
            setActiveGroupingLevel(groupingLevels[1].id);
            return;
        }
        setActiveGroupingLevel(groupingLevels[0].id);
    }
    if (isLoading) {
        return <loadingIndicator_1.default />;
    }
    if (error) {
        return (<react_1.default.Fragment>
        <errorMessage_1.default onRetry={fetchGroupingLevels} groupId={groupId} error={error} projSlug={projSlug} orgSlug={organization.slug} hasProjectWriteAccess={organization.access.includes('project:write')}/>
        <LinkFooter />
      </react_1.default.Fragment>);
    }
    if (!activeGroupingLevelDetails.length) {
        return <loadingIndicator_1.default />;
    }
    const links = (0, parseLinkHeader_1.default)(pagination);
    const hasMore = ((_a = links.previous) === null || _a === void 0 ? void 0 : _a.results) || ((_b = links.next) === null || _b === void 0 ? void 0 : _b.results);
    const paginationCurrentQuantity = activeGroupingLevelDetails.length;
    return (<Wrapper>
      <Header>
        {(0, locale_1.t)('This issue is an aggregate of multiple events that sentry determined originate from the same root-cause. Use this page to explore more detailed groupings that exist within this issue.')}
      </Header>
      <Body>
        <SliderWrapper>
          {(0, locale_1.t)('Fewer issues')}
          <StyledRangeSlider name="grouping-level" allowedValues={groupingLevels.map(groupingLevel => Number(groupingLevel.id))} value={activeGroupingLevel !== null && activeGroupingLevel !== void 0 ? activeGroupingLevel : 0} onChange={handleSetActiveGroupingLevel} showLabel={false}/>
          {(0, locale_1.t)('More issues')}
        </SliderWrapper>
        <Content isReloading={isGroupingLevelDetailsLoading}>
          <StyledPanelTable headers={['', (0, locale_1.t)('Events')]}>
            {activeGroupingLevelDetails.map(({ hash, title, metadata, latestEvent, eventCount }) => {
            // XXX(markus): Ugly hack to make NewIssue show the right things.
            return (<newIssue_1.default key={hash} sampleEvent={Object.assign(Object.assign({}, latestEvent), { metadata: Object.assign(Object.assign({}, (metadata || latestEvent.metadata)), { current_level: activeGroupingLevel }), title: title || latestEvent.title })} eventCount={eventCount} organization={organization}/>);
        })}
          </StyledPanelTable>
          <StyledPagination pageLinks={pagination} disabled={isGroupingLevelDetailsLoading} caption={(0, locale_1.tct)('Showing [current] of [total] [result]', {
            result: hasMore
                ? (0, locale_1.t)('results')
                : (0, locale_1.tn)('result', 'results', paginationCurrentQuantity),
            current: paginationCurrentQuantity,
            total: hasMore
                ? `${paginationCurrentQuantity}+`
                : paginationCurrentQuantity,
        })}/>
        </Content>
      </Body>
      <LinkFooter />
    </Wrapper>);
}
exports.default = (0, withApi_1.default)(Grouping);
const StyledIconMegaphone = (0, styled_1.default)(icons_1.IconMegaphone) `
  margin-right: ${(0, space_1.default)(0.5)};
`;
const Wrapper = (0, styled_1.default)('div') `
  flex: 1;
  display: grid;
  align-content: flex-start;
  margin: -${(0, space_1.default)(3)} -${(0, space_1.default)(4)};
  padding: ${(0, space_1.default)(3)} ${(0, space_1.default)(4)};
`;
const Header = (0, styled_1.default)('p') `
  && {
    margin-bottom: ${(0, space_1.default)(2)};
  }
`;
const Footer = (0, styled_1.default)('p') `
  && {
    margin-top: ${(0, space_1.default)(2)};
  }
`;
const Body = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
`;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  grid-template-columns: 1fr minmax(60px, auto);
  > * {
    padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(2)};
    :nth-child(-n + 2) {
      padding: ${(0, space_1.default)(2)};
    }
    :nth-child(2n) {
      display: flex;
      text-align: right;
      justify-content: flex-end;
    }
  }

  @media (min-width: ${p => p.theme.breakpoints[3]}) {
    grid-template-columns: 1fr minmax(80px, auto);
  }
`;
const StyledPagination = (0, styled_1.default)(pagination_1.default) `
  margin-top: 0;
`;
const Content = (0, styled_1.default)('div') `
  ${p => p.isReloading &&
    `
      ${StyledPanelTable}, ${StyledPagination} {
        opacity: 0.5;
        pointer-events: none;
      }
    `}
`;
const SliderWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
  grid-template-columns: max-content max-content;
  justify-content: space-between;
  align-items: flex-start;
  position: relative;
  font-size: ${p => p.theme.fontSizeMedium};
  color: ${p => p.theme.subText};
  padding-bottom: ${(0, space_1.default)(2)};

  @media (min-width: 700px) {
    grid-template-columns: max-content minmax(270px, auto) max-content;
    align-items: center;
    justify-content: flex-start;
    padding-bottom: 0;
  }
`;
const StyledRangeSlider = (0, styled_1.default)(rangeSlider_1.default) `
  ${rangeSlider_1.Slider} {
    background: transparent;
    margin-top: 0;
    margin-bottom: 0;

    ::-ms-thumb {
      box-shadow: 0 0 0 3px ${p => p.theme.backgroundSecondary};
    }

    ::-moz-range-thumb {
      box-shadow: 0 0 0 3px ${p => p.theme.backgroundSecondary};
    }

    ::-webkit-slider-thumb {
      box-shadow: 0 0 0 3px ${p => p.theme.backgroundSecondary};
    }
  }

  position: absolute;
  bottom: 0;
  left: ${(0, space_1.default)(1.5)};
  right: ${(0, space_1.default)(1.5)};

  @media (min-width: 700px) {
    position: static;
    left: auto;
    right: auto;
  }
`;
//# sourceMappingURL=grouping.jsx.map