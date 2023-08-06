Object.defineProperty(exports, "__esModule", { value: true });
exports.modalCss = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const sortBy_1 = (0, tslib_1.__importDefault)(require("lodash/sortBy"));
const indicator_1 = require("app/actionCreators/indicator");
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugFiles_1 = require("app/types/debugFiles");
const debugImage_1 = require("app/types/debugImage");
const displayReprocessEventAction_1 = require("app/utils/displayReprocessEventAction");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const utils_1 = require("app/views/settings/projectDebugFiles/utils");
const utils_2 = require("../utils");
const candidates_1 = (0, tslib_1.__importDefault)(require("./candidates"));
const generalInfo_1 = (0, tslib_1.__importDefault)(require("./generalInfo"));
const reprocessAlert_1 = (0, tslib_1.__importDefault)(require("./reprocessAlert"));
const utils_3 = require("./utils");
class DebugImageDetails extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.handleDelete = (debugId) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, projSlug } = this.props;
            this.setState({ loading: true });
            try {
                yield this.api.requestPromise(`/projects/${organization.slug}/${projSlug}/files/dsyms/?id=${debugId}`, { method: 'DELETE' });
                this.fetchData();
            }
            catch (_a) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred while deleting the debug file.'));
                this.setState({ loading: false });
            }
        });
    }
    getDefaultState() {
        return Object.assign(Object.assign({}, super.getDefaultState()), { debugFiles: [] });
    }
    componentDidUpdate(prevProps, prevState) {
        if (!prevProps.image && !!this.props.image) {
            this.remountComponent();
        }
        super.componentDidUpdate(prevProps, prevState);
    }
    getUplodedDebugFiles(candidates) {
        return candidates.find(candidate => candidate.source === utils_3.INTERNAL_SOURCE);
    }
    getEndpoints() {
        const { organization, projSlug, image } = this.props;
        if (!image) {
            return [];
        }
        const { debug_id, candidates = [] } = image;
        const uploadedDebugFiles = this.getUplodedDebugFiles(candidates);
        const endpoints = [];
        if (uploadedDebugFiles) {
            endpoints.push([
                'debugFiles',
                `/projects/${organization.slug}/${projSlug}/files/dsyms/?debug_id=${debug_id}`,
                {
                    query: {
                        file_formats: ['breakpad', 'macho', 'elf', 'pe', 'pdb', 'sourcebundle'],
                    },
                },
            ]);
        }
        return endpoints;
    }
    sortCandidates(candidates, unAppliedCandidates) {
        const [noPermissionCandidates, restNoPermissionCandidates] = (0, partition_1.default)(candidates, candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.NO_PERMISSION);
        const [malFormedCandidates, restMalFormedCandidates] = (0, partition_1.default)(restNoPermissionCandidates, candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.MALFORMED);
        const [errorCandidates, restErrorCandidates] = (0, partition_1.default)(restMalFormedCandidates, candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.ERROR);
        const [okCandidates, restOKCandidates] = (0, partition_1.default)(restErrorCandidates, candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.OK);
        const [deletedCandidates, notFoundCandidates] = (0, partition_1.default)(restOKCandidates, candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.DELETED);
        return [
            ...(0, sortBy_1.default)(noPermissionCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(malFormedCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(errorCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(okCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(deletedCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(unAppliedCandidates, ['source_name', 'location']),
            ...(0, sortBy_1.default)(notFoundCandidates, ['source_name', 'location']),
        ];
    }
    getCandidates() {
        const { debugFiles, loading } = this.state;
        const { image } = this.props;
        const { candidates = [] } = image !== null && image !== void 0 ? image : {};
        if (!debugFiles || loading) {
            return candidates;
        }
        const debugFileCandidates = candidates.map((_a) => {
            var { location } = _a, candidate = (0, tslib_1.__rest)(_a, ["location"]);
            return (Object.assign(Object.assign({}, candidate), { location: (location === null || location === void 0 ? void 0 : location.includes(utils_3.INTERNAL_SOURCE_LOCATION))
                    ? location.split(utils_3.INTERNAL_SOURCE_LOCATION)[1]
                    : location }));
        });
        const candidateLocations = new Set(debugFileCandidates.map(({ location }) => location).filter(location => !!location));
        const [unAppliedDebugFiles, appliedDebugFiles] = (0, partition_1.default)(debugFiles, debugFile => !candidateLocations.has(debugFile.id));
        const unAppliedCandidates = unAppliedDebugFiles.map(debugFile => {
            var _a;
            const { data, symbolType, objectName: filename, id: location, size, dateCreated, cpuName, } = debugFile;
            const features = (_a = data === null || data === void 0 ? void 0 : data.features) !== null && _a !== void 0 ? _a : [];
            return {
                download: {
                    status: debugImage_1.CandidateDownloadStatus.UNAPPLIED,
                    features: {
                        has_sources: features.includes(debugFiles_1.DebugFileFeature.SOURCES),
                        has_debug_info: features.includes(debugFiles_1.DebugFileFeature.DEBUG),
                        has_unwind_info: features.includes(debugFiles_1.DebugFileFeature.UNWIND),
                        has_symbols: features.includes(debugFiles_1.DebugFileFeature.SYMTAB),
                    },
                },
                cpuName,
                location,
                filename,
                size,
                dateCreated,
                symbolType,
                fileType: (0, utils_1.getFileType)(debugFile),
                source: utils_3.INTERNAL_SOURCE,
                source_name: (0, locale_1.t)('Sentry'),
            };
        });
        const [debugFileInternalOkCandidates, debugFileOtherCandidates] = (0, partition_1.default)(debugFileCandidates, debugFileCandidate => debugFileCandidate.download.status === debugImage_1.CandidateDownloadStatus.OK &&
            debugFileCandidate.source === utils_3.INTERNAL_SOURCE);
        const convertedDebugFileInternalOkCandidates = debugFileInternalOkCandidates.map(debugFileOkCandidate => {
            const internalDebugFileInfo = appliedDebugFiles.find(appliedDebugFile => appliedDebugFile.id === debugFileOkCandidate.location);
            if (!internalDebugFileInfo) {
                return Object.assign(Object.assign({}, debugFileOkCandidate), { download: Object.assign(Object.assign({}, debugFileOkCandidate.download), { status: debugImage_1.CandidateDownloadStatus.DELETED }) });
            }
            const { symbolType, objectName: filename, id: location, size, dateCreated, cpuName, } = internalDebugFileInfo;
            return Object.assign(Object.assign({}, debugFileOkCandidate), { cpuName,
                location,
                filename,
                size,
                dateCreated,
                symbolType, fileType: (0, utils_1.getFileType)(internalDebugFileInfo) });
        });
        return this.sortCandidates([
            ...convertedDebugFileInternalOkCandidates,
            ...debugFileOtherCandidates,
        ], unAppliedCandidates);
    }
    getDebugFilesSettingsLink() {
        const { organization, projSlug, image } = this.props;
        const orgSlug = organization.slug;
        const debugId = image === null || image === void 0 ? void 0 : image.debug_id;
        if (!orgSlug || !projSlug || !debugId) {
            return undefined;
        }
        return `/settings/${orgSlug}/projects/${projSlug}/debug-symbols/?query=${debugId}`;
    }
    renderBody() {
        const { Header, Body, Footer, image, organization, projSlug, event, onReprocessEvent } = this.props;
        const { loading } = this.state;
        const { code_file, status } = image !== null && image !== void 0 ? image : {};
        const debugFilesSettingsLink = this.getDebugFilesSettingsLink();
        const candidates = this.getCandidates();
        const baseUrl = this.api.baseUrl;
        const fileName = (0, utils_2.getFileName)(code_file);
        const haveCandidatesUnappliedDebugFile = candidates.some(candidate => candidate.download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED);
        const hasReprocessWarning = haveCandidatesUnappliedDebugFile &&
            (0, displayReprocessEventAction_1.displayReprocessEventAction)(organization.features, event) &&
            !!onReprocessEvent;
        return (<react_1.Fragment>
        <Header closeButton>
          <Title>
            {(0, locale_1.t)('Image')}
            <FileName>{fileName !== null && fileName !== void 0 ? fileName : (0, locale_1.t)('Unknown')}</FileName>
          </Title>
        </Header>
        <Body>
          <Content>
            <generalInfo_1.default image={image}/>
            {hasReprocessWarning && (<reprocessAlert_1.default api={this.api} orgSlug={organization.slug} projSlug={projSlug} eventId={event.id} onReprocessEvent={onReprocessEvent}/>)}
            <candidates_1.default imageStatus={status} candidates={candidates} organization={organization} projSlug={projSlug} baseUrl={baseUrl} isLoading={loading} eventDateReceived={event.dateReceived} onDelete={this.handleDelete} hasReprocessWarning={hasReprocessWarning}/>
          </Content>
        </Body>
        <Footer>
          <StyledButtonBar gap={1}>
            <button_1.default href="https://docs.sentry.io/platforms/native/data-management/debug-files/" external>
              {(0, locale_1.t)('Read the docs')}
            </button_1.default>
            {debugFilesSettingsLink && (<button_1.default title={(0, locale_1.t)('Search for this debug file in all images for the %s project', projSlug)} to={debugFilesSettingsLink}>
                {(0, locale_1.t)('Open in Settings')}
              </button_1.default>)}
          </StyledButtonBar>
        </Footer>
      </react_1.Fragment>);
    }
}
exports.default = DebugImageDetails;
const Content = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
  font-size: ${p => p.theme.fontSizeMedium};
`;
const Title = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  align-items: center;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  max-width: calc(100% - 40px);
  word-break: break-all;
`;
const FileName = (0, styled_1.default)('span') `
  font-family: ${p => p.theme.text.familyMono};
`;
const StyledButtonBar = (0, styled_1.default)(buttonBar_1.default) `
  white-space: nowrap;
`;
exports.modalCss = (0, react_2.css) `
  [role='document'] {
    overflow: initial;
  }

  @media (min-width: ${theme_1.default.breakpoints[0]}) {
    width: 90%;
  }

  @media (min-width: ${theme_1.default.breakpoints[3]}) {
    width: 70%;
  }

  @media (min-width: ${theme_1.default.breakpoints[4]}) {
    width: 50%;
  }
`;
//# sourceMappingURL=index.jsx.map