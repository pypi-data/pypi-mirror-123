Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isNil_1 = (0, tslib_1.__importDefault)(require("lodash/isNil"));
const access_1 = (0, tslib_1.__importDefault)(require("app/components/acl/access"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const debugFileFeature_1 = (0, tslib_1.__importDefault)(require("app/components/debugFileFeature"));
const utils_1 = require("app/components/events/interfaces/utils");
const panels_1 = require("app/components/panels");
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("./utils");
const IMAGE_ADDR_LEN = 12;
function getImageStatusText(status) {
    switch (status) {
        case 'found':
            return (0, locale_1.t)('ok');
        case 'unused':
            return (0, locale_1.t)('unused');
        case 'missing':
            return (0, locale_1.t)('missing');
        case 'malformed':
        case 'fetching_failed':
        case 'timeout':
        case 'other':
            return (0, locale_1.t)('failed');
        default:
            return null;
    }
}
function getImageStatusDetails(status) {
    switch (status) {
        case 'found':
            return (0, locale_1.t)('Debug information for this image was found and successfully processed.');
        case 'unused':
            return (0, locale_1.t)('The image was not required for processing the stack trace.');
        case 'missing':
            return (0, locale_1.t)('No debug information could be found in any of the specified sources.');
        case 'malformed':
            return (0, locale_1.t)('The debug information file for this image failed to process.');
        case 'timeout':
        case 'fetching_failed':
            return (0, locale_1.t)('The debug information file for this image could not be downloaded.');
        case 'other':
            return (0, locale_1.t)('An internal error occurred while handling this image.');
        default:
            return null;
    }
}
const DebugImage = React.memo(({ image, organization, projectId, showDetails, style }) => {
    const orgSlug = organization.slug;
    const getSettingsLink = () => {
        if (!orgSlug || !projectId || !image.debug_id) {
            return null;
        }
        return `/settings/${orgSlug}/projects/${projectId}/debug-symbols/?query=${image.debug_id}`;
    };
    const renderStatus = (title, status) => {
        if ((0, isNil_1.default)(status)) {
            return null;
        }
        const text = getImageStatusText(status);
        if (!text) {
            return null;
        }
        return (<SymbolicationStatus>
          <tooltip_1.default title={getImageStatusDetails(status)}>
            <span>
              <ImageProp>{title}</ImageProp>: {text}
            </span>
          </tooltip_1.default>
        </SymbolicationStatus>);
    };
    const combinedStatus = (0, utils_2.combineStatus)(image.debug_status, image.unwind_status);
    const [startAddress, endAddress] = (0, utils_1.getImageRange)(image);
    const renderIconElement = () => {
        switch (combinedStatus) {
            case 'unused':
                return (<IconWrapper>
              <icons_1.IconCircle />
            </IconWrapper>);
            case 'found':
                return (<IconWrapper>
              <icons_1.IconCheckmark isCircled color="green300"/>
            </IconWrapper>);
            default:
                return (<IconWrapper>
              <icons_1.IconFlag color="red300"/>
            </IconWrapper>);
        }
    };
    const codeFile = (0, utils_2.getFileName)(image.code_file);
    const debugFile = image.debug_file && (0, utils_2.getFileName)(image.debug_file);
    // The debug file is only realistically set on Windows. All other platforms
    // either leave it empty or set it to a filename thats equal to the code
    // file name. In this case, do not show it.
    const showDebugFile = debugFile && codeFile !== debugFile;
    // Availability only makes sense if the image is actually referenced.
    // Otherwise, the processing pipeline does not resolve this kind of
    // information and it will always be false.
    const showAvailability = !(0, isNil_1.default)(image.features) && combinedStatus !== 'unused';
    // The code id is sometimes missing, and sometimes set to the equivalent of
    // the debug id (e.g. for Mach symbols). In this case, it is redundant
    // information and we do not want to show it.
    const showCodeId = !!image.code_id && image.code_id !== image.debug_id;
    // Old versions of the event pipeline did not store the symbolication
    // status. In this case, default to display the debug_id instead of stack
    // unwind information.
    const legacyRender = (0, isNil_1.default)(image.debug_status);
    const debugIdElement = (<ImageSubtext>
        <ImageProp>{(0, locale_1.t)('Debug ID')}</ImageProp>: <Formatted>{image.debug_id}</Formatted>
      </ImageSubtext>);
    const formattedImageStartAddress = startAddress ? (<Formatted>{(0, utils_1.formatAddress)(startAddress, IMAGE_ADDR_LEN)}</Formatted>) : null;
    const formattedImageEndAddress = endAddress ? (<Formatted>{(0, utils_1.formatAddress)(endAddress, IMAGE_ADDR_LEN)}</Formatted>) : null;
    return (<DebugImageItem style={style}>
        <ImageInfoGroup>{renderIconElement()}</ImageInfoGroup>

        <ImageInfoGroup>
          {startAddress && endAddress ? (<React.Fragment>
              {formattedImageStartAddress}
              {' \u2013 '}
              <AddressDivider />
              {formattedImageEndAddress}
            </React.Fragment>) : null}
        </ImageInfoGroup>

        <ImageInfoGroup fullWidth>
          <ImageTitle>
            <tooltip_1.default title={image.code_file}>
              <CodeFile>{codeFile}</CodeFile>
            </tooltip_1.default>
            {showDebugFile && <DebugFile> ({debugFile})</DebugFile>}
          </ImageTitle>

          {legacyRender ? (debugIdElement) : (<StatusLine>
              {renderStatus((0, locale_1.t)('Stack Unwinding'), image.unwind_status)}
              {renderStatus((0, locale_1.t)('Symbolication'), image.debug_status)}
            </StatusLine>)}

          {showDetails && (<React.Fragment>
              {showAvailability && (<ImageSubtext>
                  <ImageProp>{(0, locale_1.t)('Availability')}</ImageProp>:
                  <debugFileFeature_1.default feature="symtab" available={image.features.has_symbols}/>
                  <debugFileFeature_1.default feature="debug" available={image.features.has_debug_info}/>
                  <debugFileFeature_1.default feature="unwind" available={image.features.has_unwind_info}/>
                  <debugFileFeature_1.default feature="sources" available={image.features.has_sources}/>
                </ImageSubtext>)}

              {!legacyRender && debugIdElement}

              {showCodeId && (<ImageSubtext>
                  <ImageProp>{(0, locale_1.t)('Code ID')}</ImageProp>:{' '}
                  <Formatted>{image.code_id}</Formatted>
                </ImageSubtext>)}

              {!!image.arch && (<ImageSubtext>
                  <ImageProp>{(0, locale_1.t)('Architecture')}</ImageProp>: {image.arch}
                </ImageSubtext>)}
            </React.Fragment>)}
        </ImageInfoGroup>

        <access_1.default access={['project:releases']}>
          {({ hasAccess }) => {
            if (!hasAccess) {
                return null;
            }
            const settingsUrl = getSettingsLink();
            if (!settingsUrl) {
                return null;
            }
            return (<ImageActions>
                <tooltip_1.default title={(0, locale_1.t)('Search for debug files in settings')}>
                  <button_1.default size="xsmall" icon={<icons_1.IconSearch size="xs"/>} to={settingsUrl}/>
                </tooltip_1.default>
              </ImageActions>);
        }}
        </access_1.default>
      </DebugImageItem>);
});
exports.default = DebugImage;
const DebugImageItem = (0, styled_1.default)(panels_1.PanelItem) `
  font-size: ${p => p.theme.fontSizeSmall};
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: grid;
    grid-gap: ${(0, space_1.default)(1)};
    position: relative;
  }
`;
const Formatted = (0, styled_1.default)('span') `
  font-family: ${p => p.theme.text.familyMono};
`;
const ImageInfoGroup = (0, styled_1.default)('div') `
  margin-left: 1em;
  flex-grow: ${p => (p.fullWidth ? 1 : null)};

  &:first-child {
    @media (min-width: ${p => p.theme.breakpoints[0]}) {
      margin-left: 0;
    }
  }
`;
const ImageActions = (0, styled_1.default)(ImageInfoGroup) `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    position: absolute;
    top: 15px;
    right: 20px;
  }
  display: flex;
  align-items: center;
`;
const ImageTitle = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeLarge};
`;
const CodeFile = (0, styled_1.default)('span') `
  font-weight: bold;
`;
const DebugFile = (0, styled_1.default)('span') `
  color: ${p => p.theme.gray300};
`;
const ImageSubtext = (0, styled_1.default)('div') `
  color: ${p => p.theme.gray300};
`;
const ImageProp = (0, styled_1.default)('span') `
  font-weight: bold;
`;
const StatusLine = (0, styled_1.default)(ImageSubtext) `
  display: flex;
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: grid;
  }
`;
const AddressDivider = (0, styled_1.default)('br') `
  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    display: none;
  }
`;
const IconWrapper = (0, styled_1.default)('span') `
  display: inline-block;
  margin-top: ${(0, space_1.default)(0.5)};
  height: 16px;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin-top: ${(0, space_1.default)(0.25)};
  }
`;
const SymbolicationStatus = (0, styled_1.default)('span') `
  flex-grow: 1;
  flex-basis: 0;
  margin-right: 1em;

  svg {
    margin-left: 0.66ex;
  }
`;
//# sourceMappingURL=debugImage.jsx.map