Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_virtualized_1 = require("react-virtualized");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const modal_1 = require("app/actionCreators/modal");
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const utils_1 = require("app/components/events/interfaces/utils");
const panels_1 = require("app/components/panels");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const debugMetaStore_1 = (0, tslib_1.__importStar)(require("app/stores/debugMetaStore"));
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugImage_1 = require("app/types/debugImage");
const utils_2 = require("app/utils");
const searchBarAction_1 = (0, tslib_1.__importDefault)(require("../searchBarAction"));
const searchBarActionFilter_1 = (0, tslib_1.__importDefault)(require("../searchBarAction/searchBarActionFilter"));
const status_1 = (0, tslib_1.__importDefault)(require("./debugImage/status"));
const debugImage_2 = (0, tslib_1.__importDefault)(require("./debugImage"));
const layout_1 = (0, tslib_1.__importDefault)(require("./layout"));
const utils_3 = require("./utils");
const IMAGE_INFO_UNAVAILABLE = '-1';
const cache = new react_virtualized_1.CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
class DebugMeta extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            searchTerm: '',
            scrollbarWidth: 0,
            filterOptions: {},
            filteredImages: [],
            filteredImagesByFilter: [],
            filteredImagesBySearch: [],
        };
        this.panelTableRef = React.createRef();
        this.listRef = null;
        this.onDebugMetaStoreChange = (store) => {
            const { searchTerm } = this.state;
            if (store.filter !== searchTerm) {
                this.setState({ searchTerm: store.filter }, this.filterImagesBySearchTerm);
            }
        };
        this.updateGrid = () => {
            if (this.listRef) {
                cache.clearAll();
                this.listRef.forceUpdateGrid();
                this.getScrollbarWidth();
            }
        };
        this.openImageDetailsModal = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { filteredImages } = this.state;
            if (!filteredImages.length) {
                return;
            }
            const { location, organization, projectId: projSlug, groupId, event } = this.props;
            const { query } = location;
            const { imageCodeId, imageDebugId } = query;
            if (!imageCodeId && !imageDebugId) {
                return;
            }
            const image = imageCodeId !== IMAGE_INFO_UNAVAILABLE || imageDebugId !== IMAGE_INFO_UNAVAILABLE
                ? filteredImages.find(({ code_id, debug_id }) => code_id === imageCodeId || debug_id === imageDebugId)
                : undefined;
            const mod = yield Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/components/events/interfaces/debugMeta-v2/debugImageDetails')));
            const { default: Modal, modalCss } = mod;
            (0, modal_1.openModal)(deps => (<Modal {...deps} image={image} organization={organization} projSlug={projSlug} event={event} onReprocessEvent={(0, utils_2.defined)(groupId) ? this.handleReprocessEvent(groupId) : undefined}/>), {
                modalCss,
                onClose: this.handleCloseImageDetailsModal,
            });
        });
        this.handleChangeFilter = (filterOptions) => {
            const { filteredImagesBySearch } = this.state;
            const filteredImagesByFilter = this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
            this.setState({ filterOptions, filteredImagesByFilter }, this.updateGrid);
        };
        this.handleChangeSearchTerm = (searchTerm = '') => {
            debugMetaStore_1.DebugMetaActions.updateFilter(searchTerm);
        };
        this.handleResetFilter = () => {
            const { filterOptions } = this.state;
            this.setState({
                filterOptions: Object.keys(filterOptions).reduce((accumulator, currentValue) => {
                    accumulator[currentValue] = filterOptions[currentValue].map(filterOption => (Object.assign(Object.assign({}, filterOption), { isChecked: false })));
                    return accumulator;
                }, {}),
            }, this.filterImagesBySearchTerm);
        };
        this.handleResetSearchBar = () => {
            this.setState(prevState => ({
                searchTerm: '',
                filteredImagesByFilter: prevState.filteredImages,
                filteredImagesBySearch: prevState.filteredImages,
            }));
        };
        this.handleOpenImageDetailsModal = (code_id, debug_id) => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { imageCodeId: code_id !== null && code_id !== void 0 ? code_id : IMAGE_INFO_UNAVAILABLE, imageDebugId: debug_id !== null && debug_id !== void 0 ? debug_id : IMAGE_INFO_UNAVAILABLE }) }));
        };
        this.handleCloseImageDetailsModal = () => {
            const { location, router } = this.props;
            router.push(Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { imageCodeId: undefined, imageDebugId: undefined }) }));
        };
        this.handleReprocessEvent = (groupId) => () => {
            const { organization } = this.props;
            (0, modal_1.openReprocessEventModal)({
                organization,
                groupId,
                onClose: this.openImageDetailsModal,
            });
        };
        this.renderRow = ({ index, key, parent, style }) => {
            const { filteredImagesByFilter: images } = this.state;
            return (<react_virtualized_1.CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <debugImage_2.default style={style} image={images[index]} onOpenImageDetailsModal={this.handleOpenImageDetailsModal}/>
      </react_virtualized_1.CellMeasurer>);
        };
    }
    componentDidMount() {
        this.unsubscribeFromDebugMetaStore = debugMetaStore_1.default.listen(this.onDebugMetaStoreChange, undefined);
        cache.clearAll();
        this.getRelevantImages();
        this.openImageDetailsModal();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
        this.openImageDetailsModal();
    }
    componentWillUnmount() {
        if (this.unsubscribeFromDebugMetaStore) {
            this.unsubscribeFromDebugMetaStore();
        }
    }
    getScrollbarWidth() {
        var _a, _b, _c, _d, _e, _f, _g;
        const panelTableWidth = (_c = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.clientWidth) !== null && _c !== void 0 ? _c : 0;
        const gridInnerWidth = (_g = (_f = (_e = (_d = this.panelTableRef) === null || _d === void 0 ? void 0 : _d.current) === null || _e === void 0 ? void 0 : _e.querySelector('.ReactVirtualized__Grid__innerScrollContainer')) === null || _f === void 0 ? void 0 : _f.clientWidth) !== null && _g !== void 0 ? _g : 0;
        const scrollbarWidth = panelTableWidth - gridInnerWidth;
        if (scrollbarWidth !== this.state.scrollbarWidth) {
            this.setState({ scrollbarWidth });
        }
    }
    isValidImage(image) {
        // in particular proguard images do not have a code file, skip them
        if (image === null || image.code_file === null || image.type === 'proguard') {
            return false;
        }
        if ((0, utils_3.getFileName)(image.code_file) === 'dyld_sim') {
            // this is only for simulator builds
            return false;
        }
        return true;
    }
    filterImage(image, searchTerm) {
        var _a, _b;
        // When searching for an address, check for the address range of the image
        // instead of an exact match.  Note that images cannot be found by index
        // if they are at 0x0.  For those relative addressing has to be used.
        if (searchTerm.indexOf('0x') === 0) {
            const needle = (0, utils_1.parseAddress)(searchTerm);
            if (needle > 0 && image.image_addr !== '0x0') {
                const [startAddress, endAddress] = (0, utils_1.getImageRange)(image); // TODO(PRISCILA): remove any
                return needle >= startAddress && needle < endAddress;
            }
        }
        // the searchTerm ending at "!" is the end of the ID search.
        const relMatch = searchTerm.match(/^\s*(.*?)!/); // debug_id!address
        const idSearchTerm = (0, utils_3.normalizeId)((relMatch === null || relMatch === void 0 ? void 0 : relMatch[1]) || searchTerm);
        return (
        // Prefix match for identifiers
        (0, utils_3.normalizeId)(image.code_id).indexOf(idSearchTerm) === 0 ||
            (0, utils_3.normalizeId)(image.debug_id).indexOf(idSearchTerm) === 0 ||
            // Any match for file paths
            (((_a = image.code_file) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_b = image.debug_file) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    }
    filterImagesBySearchTerm() {
        const { filteredImages, filterOptions, searchTerm } = this.state;
        const filteredImagesBySearch = filteredImages.filter(image => this.filterImage(image, searchTerm.toLowerCase()));
        const filteredImagesByFilter = this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
        this.setState({
            filteredImagesBySearch,
            filteredImagesByFilter,
        }, this.updateGrid);
    }
    getPanelBodyHeight() {
        var _a, _b;
        const panelTableHeight = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelTableHeight) {
            return;
        }
        this.setState({ panelTableHeight });
    }
    getRelevantImages() {
        const { data } = this.props;
        const { images } = data;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        const relevantImages = images.filter(this.isValidImage);
        if (!relevantImages.length) {
            return;
        }
        const formattedRelevantImages = relevantImages.map(releventImage => {
            const { debug_status, unwind_status } = releventImage;
            return Object.assign(Object.assign({}, releventImage), { status: (0, utils_3.combineStatus)(debug_status, unwind_status) });
        });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        formattedRelevantImages.sort((a, b) => (0, utils_1.parseAddress)(a.image_addr) - (0, utils_1.parseAddress)(b.image_addr));
        const unusedImages = [];
        const usedImages = formattedRelevantImages.filter(image => {
            if (image.debug_status === debugImage_1.ImageStatus.UNUSED) {
                unusedImages.push(image);
                return false;
            }
            return true;
        });
        const filteredImages = [...usedImages, ...unusedImages];
        const filterOptions = this.getFilterOptions(filteredImages);
        this.setState({
            filteredImages,
            filterOptions,
            filteredImagesByFilter: this.getFilteredImagesByFilter(filteredImages, filterOptions),
            filteredImagesBySearch: filteredImages,
        });
    }
    getFilterOptions(images) {
        return {
            [(0, locale_1.t)('Status')]: [...new Set(images.map(image => image.status))].map(status => ({
                id: status,
                symbol: <status_1.default status={status}/>,
                isChecked: status !== debugImage_1.ImageStatus.UNUSED,
            })),
        };
    }
    getFilteredImagesByFilter(filteredImages, filterOptions) {
        const checkedOptions = new Set(Object.values(filterOptions)[0]
            .filter(filterOption => filterOption.isChecked)
            .map(option => option.id));
        if (![...checkedOptions].length) {
            return filteredImages;
        }
        return filteredImages.filter(image => checkedOptions.has(image.status));
    }
    renderList() {
        const { filteredImagesByFilter: images, panelTableHeight } = this.state;
        if (!panelTableHeight) {
            return images.map((image, index) => (<debugImage_2.default key={index} image={image} onOpenImageDetailsModal={this.handleOpenImageDetailsModal}/>));
        }
        return (<react_virtualized_1.AutoSizer disableHeight onResize={this.updateGrid}>
        {({ width }) => (<StyledList ref={(el) => {
                    this.listRef = el;
                }} deferredMeasurementCache={cache} height={utils_3.IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT} overscanRowCount={5} rowCount={images.length} rowHeight={cache.rowHeight} rowRenderer={this.renderRow} width={width} isScrolling={false}/>)}
      </react_virtualized_1.AutoSizer>);
    }
    getEmptyMessage() {
        const { searchTerm, filteredImagesByFilter: images, filterOptions } = this.state;
        if (!!images.length) {
            return {};
        }
        if (searchTerm && !images.length) {
            const hasActiveFilter = Object.values(filterOptions)
                .flatMap(filterOption => filterOption)
                .find(filterOption => filterOption.isChecked);
            return {
                emptyMessage: (0, locale_1.t)('Sorry, no images match your search query'),
                emptyAction: hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
            {(0, locale_1.t)('Reset filter')}
          </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
            {(0, locale_1.t)('Clear search bar')}
          </button_1.default>),
            };
        }
        return {
            emptyMessage: (0, locale_1.t)('There are no images to be displayed'),
        };
    }
    render() {
        var _a;
        const { searchTerm, filterOptions, scrollbarWidth, filteredImagesByFilter: filteredImages, } = this.state;
        const { data } = this.props;
        const { images } = data;
        if ((0, utils_3.shouldSkipSection)(filteredImages, images)) {
            return null;
        }
        const displayFilter = ((_a = Object.values(filterOptions !== null && filterOptions !== void 0 ? filterOptions : {})[0]) !== null && _a !== void 0 ? _a : []).length > 1;
        return (<StyledEventDataSection type="images-loaded" title={<TitleWrapper>
            <guideAnchor_1.default target="images-loaded" position="bottom">
              <Title>{(0, locale_1.t)('Images Loaded')}</Title>
            </guideAnchor_1.default>
            <questionTooltip_1.default size="xs" position="top" title={(0, locale_1.t)('A list of dynamic librarys or shared objects loaded into process memory at the time of the crash. Images contribute application code that is referenced in stack traces.')}/>
          </TitleWrapper>} actions={<StyledSearchBarAction placeholder={(0, locale_1.t)('Search images loaded')} onChange={value => this.handleChangeSearchTerm(value)} query={searchTerm} filter={displayFilter ? (<searchBarActionFilter_1.default onChange={this.handleChangeFilter} options={filterOptions}/>) : undefined}/>} wrapTitle={false} isCentered>
        <StyledPanelTable isEmpty={!filteredImages.length} scrollbarWidth={scrollbarWidth} headers={[(0, locale_1.t)('Status'), (0, locale_1.t)('Image'), (0, locale_1.t)('Processing'), (0, locale_1.t)('Details'), '']} {...this.getEmptyMessage()}>
          <div ref={this.panelTableRef}>{this.renderList()}</div>
        </StyledPanelTable>
      </StyledEventDataSection>);
    }
}
DebugMeta.defaultProps = {
    data: { images: [] },
};
exports.default = (0, react_router_1.withRouter)(DebugMeta);
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  padding-bottom: ${(0, space_1.default)(4)};

  /* to increase specificity */
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-bottom: ${(0, space_1.default)(2)};
  }
`;
const StyledPanelTable = (0, styled_1.default)(panels_1.PanelTable) `
  overflow: hidden;
  > * {
    :nth-child(-n + 5) {
      ${overflowEllipsis_1.default};
      border-bottom: 1px solid ${p => p.theme.border};
      :nth-child(5n) {
        height: 100%;
        ${p => !p.scrollbarWidth && `display: none`}
      }
    }

    :nth-child(n + 6) {
      grid-column: 1/-1;
      ${p => !p.isEmpty &&
    `
          display: grid;
          padding: 0;
        `}
    }
  }

  ${p => (0, layout_1.default)(p.theme, p.scrollbarWidth)}
`;
const TitleWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(0.5)};
  align-items: center;
  padding: ${(0, space_1.default)(0.75)} 0;
`;
const Title = (0, styled_1.default)('h3') `
  margin-bottom: 0;
  padding: 0 !important;
  height: 14px;
`;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
const StyledList = (0, styled_1.default)(react_virtualized_1.List) `
  height: auto !important;
  max-height: ${p => p.height}px;
  overflow-y: auto !important;
  outline: none;
`;
const StyledSearchBarAction = (0, styled_1.default)(searchBarAction_1.default) `
  z-index: 1;
`;
//# sourceMappingURL=index.jsx.map