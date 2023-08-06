Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const capitalize_1 = (0, tslib_1.__importDefault)(require("lodash/capitalize"));
const moment_timezone_1 = (0, tslib_1.__importDefault)(require("moment-timezone"));
const dateTime_1 = (0, tslib_1.__importDefault)(require("app/components/dateTime"));
const fileSize_1 = (0, tslib_1.__importDefault)(require("app/components/fileSize"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const debugImage_1 = require("app/types/debugImage");
const item_1 = (0, tslib_1.__importDefault)(require("../../../processing/item"));
const list_1 = (0, tslib_1.__importDefault)(require("../../../processing/list"));
const utils_1 = require("../../utils");
const divider_1 = (0, tslib_1.__importDefault)(require("./divider"));
const features_1 = (0, tslib_1.__importDefault)(require("./features"));
const processingIcon_1 = (0, tslib_1.__importDefault)(require("./processingIcon"));
function Information({ candidate, isInternalSource, hasReprocessWarning, eventDateReceived, }) {
    const { source_name, source, location, download } = candidate;
    function getFilenameOrLocation() {
        if (candidate.download.status === debugImage_1.CandidateDownloadStatus.UNAPPLIED ||
            (candidate.download.status === debugImage_1.CandidateDownloadStatus.OK && isInternalSource)) {
            const { symbolType, filename } = candidate;
            return symbolType === debugImage_1.SymbolType.PROGUARD && filename === 'proguard-mapping'
                ? null
                : filename;
        }
        if (location && !isInternalSource) {
            return location;
        }
        return null;
    }
    function getTimeSinceData(dateCreated) {
        const dateTime = <dateTime_1.default date={dateCreated}/>;
        if (candidate.download.status !== debugImage_1.CandidateDownloadStatus.UNAPPLIED) {
            return {
                tooltipDesc: dateTime,
                displayIcon: false,
            };
        }
        const uploadedBeforeEvent = (0, moment_timezone_1.default)(dateCreated).isBefore(eventDateReceived);
        if (uploadedBeforeEvent) {
            if (hasReprocessWarning) {
                return {
                    tooltipDesc: (<React.Fragment>
              {(0, locale_1.tct)('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate. To apply new debug information, reprocess this issue.', {
                            when: (0, moment_timezone_1.default)(eventDateReceived).from(dateCreated, true),
                        })}
              <DateTimeWrapper>{dateTime}</DateTimeWrapper>
            </React.Fragment>),
                    displayIcon: true,
                };
            }
            const uplodadedMinutesDiff = (0, moment_timezone_1.default)(eventDateReceived).diff(dateCreated, 'minutes');
            if (uplodadedMinutesDiff >= 60) {
                return {
                    tooltipDesc: dateTime,
                    displayIcon: false,
                };
            }
            return {
                tooltipDesc: (<React.Fragment>
            {(0, locale_1.tct)('This debug file was uploaded [when] before this event. It takes up to 1 hour for new files to propagate.', {
                        when: (0, moment_timezone_1.default)(eventDateReceived).from(dateCreated, true),
                    })}
            <DateTimeWrapper>{dateTime}</DateTimeWrapper>
          </React.Fragment>),
                displayIcon: true,
            };
        }
        if (hasReprocessWarning) {
            return {
                tooltipDesc: (<React.Fragment>
            {(0, locale_1.tct)('This debug file was uploaded [when] after this event. To apply new debug information, reprocess this issue.', {
                        when: (0, moment_timezone_1.default)(dateCreated).from(eventDateReceived, true),
                    })}
            <DateTimeWrapper>{dateTime}</DateTimeWrapper>
          </React.Fragment>),
                displayIcon: true,
            };
        }
        return {
            tooltipDesc: (<React.Fragment>
          {(0, locale_1.tct)('This debug file was uploaded [when] after this event.', {
                    when: (0, moment_timezone_1.default)(eventDateReceived).from(dateCreated, true),
                })}
          <DateTimeWrapper>{dateTime}</DateTimeWrapper>
        </React.Fragment>),
            displayIcon: true,
        };
    }
    function renderProcessingInfo() {
        if (candidate.download.status !== debugImage_1.CandidateDownloadStatus.OK &&
            candidate.download.status !== debugImage_1.CandidateDownloadStatus.DELETED) {
            return null;
        }
        const items = [];
        const { debug, unwind } = candidate;
        if (debug) {
            items.push(<item_1.default key="symbolication" type="symbolication" icon={<processingIcon_1.default processingInfo={debug}/>}/>);
        }
        if (unwind) {
            items.push(<item_1.default key="stack_unwinding" type="stack_unwinding" icon={<processingIcon_1.default processingInfo={unwind}/>}/>);
        }
        if (!items.length) {
            return null;
        }
        return (<React.Fragment>
        <StyledProcessingList items={items}/>
        <divider_1.default />
      </React.Fragment>);
    }
    function renderExtraDetails() {
        if ((candidate.download.status !== debugImage_1.CandidateDownloadStatus.UNAPPLIED &&
            candidate.download.status !== debugImage_1.CandidateDownloadStatus.OK) ||
            source !== utils_1.INTERNAL_SOURCE) {
            return null;
        }
        const { symbolType, fileType, cpuName, size, dateCreated } = candidate;
        const { tooltipDesc, displayIcon } = getTimeSinceData(dateCreated);
        return (<React.Fragment>
        <tooltip_1.default title={tooltipDesc}>
          <TimeSinceWrapper>
            {displayIcon && <icons_1.IconWarning color="red300" size="xs"/>}
            {(0, locale_1.tct)('Uploaded [timesince]', {
                timesince: <timeSince_1.default disabledAbsoluteTooltip date={dateCreated}/>,
            })}
          </TimeSinceWrapper>
        </tooltip_1.default>
        <divider_1.default />
        <fileSize_1.default bytes={size}/>
        <divider_1.default />
        <span>
          {symbolType === debugImage_1.SymbolType.PROGUARD && cpuName === 'any'
                ? (0, locale_1.t)('proguard mapping')
                : `${symbolType}${fileType ? ` ${fileType}` : ''}`}
        </span>
        <divider_1.default />
      </React.Fragment>);
    }
    const filenameOrLocation = getFilenameOrLocation();
    return (<Wrapper>
      <div>
        <strong data-test-id="source_name">
          {source_name ? (0, capitalize_1.default)(source_name) : (0, locale_1.t)('Unknown')}
        </strong>
        {filenameOrLocation && (<FilenameOrLocation>{filenameOrLocation}</FilenameOrLocation>)}
      </div>
      <Details>
        {renderExtraDetails()}
        {renderProcessingInfo()}
        <features_1.default download={download}/>
      </Details>
    </Wrapper>);
}
exports.default = Information;
const Wrapper = (0, styled_1.default)('div') `
  white-space: pre-wrap;
  word-break: break-all;
  max-width: 100%;
`;
const FilenameOrLocation = (0, styled_1.default)('span') `
  padding-left: ${(0, space_1.default)(1)};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const Details = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  grid-gap: ${(0, space_1.default)(1)};
  color: ${p => p.theme.gray400};
  font-size: ${p => p.theme.fontSizeSmall};
`;
const TimeSinceWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: max-content 1fr;
  align-items: center;
  grid-gap: ${(0, space_1.default)(0.5)};
  font-variant-numeric: tabular-nums;
`;
const DateTimeWrapper = (0, styled_1.default)('div') `
  padding-top: ${(0, space_1.default)(1)};
  font-variant-numeric: tabular-nums;
`;
const StyledProcessingList = (0, styled_1.default)(list_1.default) `
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  grid-gap: ${(0, space_1.default)(1)};
`;
//# sourceMappingURL=index.jsx.map