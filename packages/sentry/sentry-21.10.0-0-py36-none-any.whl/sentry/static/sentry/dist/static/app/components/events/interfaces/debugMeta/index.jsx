Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_virtualized_1 = require("react-virtualized");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const checkbox_1 = (0, tslib_1.__importDefault)(require("app/components/checkbox"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const imageForBar_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/imageForBar"));
const utils_1 = require("app/components/events/interfaces/utils");
const panels_1 = require("app/components/panels");
const searchBar_1 = (0, tslib_1.__importDefault)(require("app/components/searchBar"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const debugMetaStore_1 = (0, tslib_1.__importStar)(require("app/stores/debugMetaStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const utils_2 = require("../debugMeta-v2/utils");
const debugImage_1 = (0, tslib_1.__importDefault)(require("./debugImage"));
const utils_3 = require("./utils");
const MIN_FILTER_LEN = 3;
const PANEL_MAX_HEIGHT = 400;
function normalizeId(id) {
    return id ? id.trim().toLowerCase().replace(/[- ]/g, '') : '';
}
const cache = new react_virtualized_1.CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
class DebugMeta extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            filter: '',
            debugImages: [],
            filteredImages: [],
            showUnused: false,
            showDetails: false,
        };
        this.panelBodyRef = React.createRef();
        this.listRef = null;
        this.onStoreChange = (store) => {
            this.setState({
                filter: store.filter,
            });
        };
        this.renderRow = ({ index, key, parent, style }) => {
            const { organization, projectId } = this.props;
            const { filteredImages, showDetails } = this.state;
            return (<react_virtualized_1.CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <debugImage_1.default style={style} image={filteredImages[index]} organization={organization} projectId={projectId} showDetails={showDetails}/>
      </react_virtualized_1.CellMeasurer>);
        };
        this.handleChangeShowUnused = (event) => {
            const showUnused = event.target.checked;
            this.setState({ showUnused });
        };
        this.handleShowUnused = () => {
            this.setState({ showUnused: true });
        };
        this.handleChangeShowDetails = (event) => {
            const showDetails = event.target.checked;
            this.setState({ showDetails });
        };
        this.handleChangeFilter = (value = '') => {
            debugMetaStore_1.DebugMetaActions.updateFilter(value);
        };
    }
    componentDidMount() {
        this.unsubscribeFromStore = debugMetaStore_1.default.listen(this.onStoreChange, undefined);
        cache.clearAll();
        this.filterImages();
    }
    componentDidUpdate(_prevProps, prevState) {
        if (prevState.showUnused !== this.state.showUnused ||
            prevState.filter !== this.state.filter) {
            this.filterImages();
        }
        if (!(0, isEqual_1.default)(prevState.foundFrame, this.state.foundFrame) ||
            this.state.showDetails !== prevState.showDetails ||
            prevState.showUnused !== this.state.showUnused ||
            (prevState.filter && !this.state.filter)) {
            this.updateGrid();
        }
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
    }
    componentWillUnmount() {
        if (this.unsubscribeFromStore) {
            this.unsubscribeFromStore();
        }
    }
    updateGrid() {
        var _a;
        cache.clearAll();
        (_a = this.listRef) === null || _a === void 0 ? void 0 : _a.forceUpdateGrid();
    }
    getPanelBodyHeight() {
        var _a, _b;
        const panelBodyHeight = (_b = (_a = this.panelBodyRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelBodyHeight) {
            return;
        }
        this.setState({ panelBodyHeight });
    }
    filterImage(image) {
        var _a, _b;
        const { showUnused, filter } = this.state;
        const searchTerm = filter.trim().toLowerCase();
        if (searchTerm.length < MIN_FILTER_LEN) {
            if (showUnused) {
                return true;
            }
            // A debug status of `null` indicates that this information is not yet
            // available in an old event. Default to showing the image.
            if (image.debug_status !== 'unused') {
                return true;
            }
            // An unwind status of `null` indicates that symbolicator did not unwind.
            // Ignore the status in this case.
            if (!(0, isNil_1.default)(image.unwind_status) && image.unwind_status !== 'unused') {
                return true;
            }
            return false;
        }
        // When searching for an address, check for the address range of the image
        // instead of an exact match.  Note that images cannot be found by index
        // if they are at 0x0.  For those relative addressing has to be used.
        if (searchTerm.indexOf('0x') === 0) {
            const needle = (0, utils_1.parseAddress)(searchTerm);
            if (needle > 0 && image.image_addr !== '0x0') {
                const [startAddress, endAddress] = (0, utils_1.getImageRange)(image);
                return needle >= startAddress && needle < endAddress;
            }
        }
        // the searchTerm ending at "!" is the end of the ID search.
        const relMatch = searchTerm.match(/^\s*(.*?)!/); // debug_id!address
        const idSearchTerm = normalizeId((relMatch === null || relMatch === void 0 ? void 0 : relMatch[1]) || searchTerm);
        return (
        // Prefix match for identifiers
        normalizeId(image.code_id).indexOf(idSearchTerm) === 0 ||
            normalizeId(image.debug_id).indexOf(idSearchTerm) === 0 ||
            // Any match for file paths
            (((_a = image.code_file) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_b = image.debug_file) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    }
    filterImages() {
        const foundFrame = this.getFrame();
        // skip null values indicating invalid debug images
        const debugImages = this.getDebugImages();
        if (!debugImages.length) {
            return;
        }
        const filteredImages = debugImages.filter(image => this.filterImage(image));
        this.setState({ debugImages, filteredImages, foundFrame });
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
    getFrame() {
        var _a, _b, _c, _d, _e;
        const { event: { entries }, } = this.props;
        const frames = (_e = (_d = (_c = (_b = (_a = entries.find(({ type }) => type === 'exception')) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.values) === null || _c === void 0 ? void 0 : _c[0]) === null || _d === void 0 ? void 0 : _d.stacktrace) === null || _e === void 0 ? void 0 : _e.frames;
        if (!frames) {
            return undefined;
        }
        const searchTerm = normalizeId(this.state.filter);
        const relMatch = searchTerm.match(/^\s*(.*?)!(.*)$/); // debug_id!address
        if (relMatch) {
            const debugImages = this.getDebugImages().map((image, idx) => [idx, image]);
            const filteredImages = debugImages.filter(([_, image]) => this.filterImage(image));
            if (filteredImages.length === 1) {
                return frames.find(frame => {
                    var _a;
                    return frame.addrMode === `rel:${filteredImages[0][0]}` &&
                        ((_a = frame.instructionAddr) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === relMatch[2];
                });
            }
            return undefined;
        }
        return frames.find(frame => { var _a; return ((_a = frame.instructionAddr) === null || _a === void 0 ? void 0 : _a.toLowerCase()) === searchTerm; });
    }
    getDebugImages() {
        const { data: { images }, } = this.props;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        const filtered = images.filter(image => this.isValidImage(image));
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        filtered.sort((a, b) => (0, utils_1.parseAddress)(a.image_addr) - (0, utils_1.parseAddress)(b.image_addr));
        return filtered;
    }
    getNoImagesMessage() {
        const { filter, showUnused, debugImages } = this.state;
        if (debugImages.length === 0) {
            return (0, locale_1.t)('No loaded images available.');
        }
        if (!showUnused && !filter) {
            return (0, locale_1.tct)('No images are referenced in the stack trace. [toggle: Show Unreferenced]', {
                toggle: <button_1.default priority="link" onClick={this.handleShowUnused}/>,
            });
        }
        return (0, locale_1.t)('Sorry, no images match your query.');
    }
    renderToolbar() {
        const { filter, showDetails, showUnused } = this.state;
        return (<ToolbarWrapper>
        <Label>
          <checkbox_1.default checked={showDetails} onChange={this.handleChangeShowDetails}/>
          {(0, locale_1.t)('details')}
        </Label>

        <Label>
          <checkbox_1.default checked={showUnused || !!filter} disabled={!!filter} onChange={this.handleChangeShowUnused}/>
          {(0, locale_1.t)('show unreferenced')}
        </Label>
        <SearchInputWrapper>
          <StyledSearchBar onChange={this.handleChangeFilter} query={filter} placeholder={(0, locale_1.t)('Search images\u2026')}/>
        </SearchInputWrapper>
      </ToolbarWrapper>);
    }
    getListHeight() {
        const { showUnused, showDetails, panelBodyHeight } = this.state;
        if (!panelBodyHeight ||
            panelBodyHeight > PANEL_MAX_HEIGHT ||
            showUnused ||
            showDetails) {
            return PANEL_MAX_HEIGHT;
        }
        return panelBodyHeight;
    }
    renderImageList() {
        const { filteredImages, showDetails, panelBodyHeight } = this.state;
        const { organization, projectId } = this.props;
        if (!panelBodyHeight) {
            return filteredImages.map(filteredImage => (<debugImage_1.default key={filteredImage.debug_id} image={filteredImage} organization={organization} projectId={projectId} showDetails={showDetails}/>));
        }
        return (<react_virtualized_1.AutoSizer disableHeight>
        {({ width }) => (<StyledList ref={(el) => {
                    this.listRef = el;
                }} deferredMeasurementCache={cache} height={this.getListHeight()} overscanRowCount={5} rowCount={filteredImages.length} rowHeight={cache.rowHeight} rowRenderer={this.renderRow} width={width} isScrolling={false}/>)}
      </react_virtualized_1.AutoSizer>);
    }
    render() {
        const { filteredImages, foundFrame } = this.state;
        const { data } = this.props;
        const { images } = data;
        if ((0, utils_2.shouldSkipSection)(filteredImages, images)) {
            return null;
        }
        return (<StyledEventDataSection type="images-loaded" title={<guideAnchor_1.default target="images-loaded" position="bottom">
            <h3>{(0, locale_1.t)('Images Loaded')}</h3>
          </guideAnchor_1.default>} actions={this.renderToolbar()} wrapTitle={false} isCentered>
        <DebugImagesPanel>
          {filteredImages.length > 0 ? (<React.Fragment>
              {foundFrame && (<imageForBar_1.default frame={foundFrame} onShowAllImages={this.handleChangeFilter}/>)}
              <panels_1.PanelBody ref={this.panelBodyRef}>{this.renderImageList()}</panels_1.PanelBody>
            </React.Fragment>) : (<emptyMessage_1.default icon={<icons_1.IconWarning size="xl"/>}>
              {this.getNoImagesMessage()}
            </emptyMessage_1.default>)}
        </DebugImagesPanel>
      </StyledEventDataSection>);
    }
}
DebugMeta.defaultProps = {
    data: { images: [] },
};
exports.default = DebugMeta;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
//
// It gives the list have a dynamic height; otherwise, in the case of filtered
// options, a list will be displayed with an empty space
const StyledList = (0, styled_1.default)(react_virtualized_1.List) `
  height: auto !important;
  max-height: ${p => p.height}px;
  outline: none;
`;
const Label = (0, styled_1.default)('label') `
  font-weight: normal;
  margin-right: 1em;
  margin-bottom: 0;
  white-space: nowrap;

  > input {
    margin-right: 1ex;
  }
`;
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    padding-bottom: ${(0, space_1.default)(4)};
  }
  /* to increase specificity */
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-bottom: ${(0, space_1.default)(2)};
  }
`;
const DebugImagesPanel = (0, styled_1.default)(panels_1.Panel) `
  margin-bottom: ${(0, space_1.default)(1)};
  max-height: ${PANEL_MAX_HEIGHT}px;
  overflow: hidden;
`;
const ToolbarWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    flex-wrap: wrap;
    margin-top: ${(0, space_1.default)(1)};
  }
`;
const SearchInputWrapper = (0, styled_1.default)('div') `
  width: 100%;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    width: 100%;
    max-width: 100%;
    margin-top: ${(0, space_1.default)(1)};
  }

  @media (min-width: ${p => p.theme.breakpoints[0]}) and (max-width: ${p => p.theme.breakpoints[3]}) {
    max-width: 180px;
    display: inline-block;
  }

  @media (min-width: ${props => props.theme.breakpoints[3]}) {
    width: 330px;
    max-width: none;
  }

  @media (min-width: 1550px) {
    width: 510px;
  }
`;
// TODO(matej): remove this once we refactor SearchBar to not use css classes
// - it could accept size as a prop
const StyledSearchBar = (0, styled_1.default)(searchBar_1.default) `
  .search-input {
    height: 30px;
  }
`;
//# sourceMappingURL=index.jsx.map