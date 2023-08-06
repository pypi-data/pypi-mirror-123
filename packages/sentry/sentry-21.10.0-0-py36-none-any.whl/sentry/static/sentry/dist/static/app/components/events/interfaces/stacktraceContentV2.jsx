Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const platformicons_1 = require("platformicons");
const list_1 = (0, tslib_1.__importDefault)(require("app/components/list"));
const listItem_1 = (0, tslib_1.__importDefault)(require("app/components/list/listItem"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const lineV2_1 = (0, tslib_1.__importDefault)(require("./frame/lineV2"));
const utils_1 = require("./utils");
function StackTraceContent({ data, platform, event, newestFirst, className, isHoverPreviewed, groupingCurrentLevel, includeSystemFrames = true, expandFirstFrame = true, }) {
    const [showingAbsoluteAddresses, setShowingAbsoluteAddresses] = (0, react_1.useState)(false);
    const [showCompleteFunctionName, setShowCompleteFunctionName] = (0, react_1.useState)(false);
    const { frames = [], framesOmitted, registers } = data;
    function findImageForAddress(address, addrMode) {
        var _a, _b;
        const images = (_b = (_a = event.entries.find(entry => entry.type === 'debugmeta')) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.images;
        return images && address
            ? images.find((img, idx) => {
                if (!addrMode || addrMode === 'abs') {
                    const [startAddress, endAddress] = (0, utils_1.getImageRange)(img);
                    return address >= startAddress && address < endAddress;
                }
                return addrMode === `rel:${idx}`;
            })
            : null;
    }
    function getClassName() {
        if (includeSystemFrames) {
            return `${className} traceback full-traceback`;
        }
        return `${className} traceback in-app-traceback`;
    }
    function isFrameUsedForGrouping(frame) {
        const { minGroupingLevel } = frame;
        if (groupingCurrentLevel === undefined || minGroupingLevel === undefined) {
            return false;
        }
        return minGroupingLevel <= groupingCurrentLevel;
    }
    function handleToggleAddresses(mouseEvent) {
        mouseEvent.stopPropagation(); // to prevent collapsing if collapsible
        setShowingAbsoluteAddresses(!showingAbsoluteAddresses);
    }
    function handleToggleFunctionName(mouseEvent) {
        mouseEvent.stopPropagation(); // to prevent collapsing if collapsible
        setShowCompleteFunctionName(!showCompleteFunctionName);
    }
    function getLastFrameIndex() {
        const inAppFrameIndexes = frames
            .map((frame, frameIndex) => {
            if (frame.inApp) {
                return frameIndex;
            }
            return undefined;
        })
            .filter(frame => frame !== undefined);
        return !inAppFrameIndexes.length
            ? frames.length - 1
            : inAppFrameIndexes[inAppFrameIndexes.length - 1];
    }
    function renderOmittedFrames(firstFrameOmitted, lastFrameOmitted) {
        return (<listItem_1.default className="frame frames-omitted">
        {(0, locale_1.t)('Frames %d until %d were omitted and not available.', firstFrameOmitted, lastFrameOmitted)}
      </listItem_1.default>);
    }
    function renderConvertedFrames() {
        var _a, _b;
        const firstFrameOmitted = (_a = framesOmitted === null || framesOmitted === void 0 ? void 0 : framesOmitted[0]) !== null && _a !== void 0 ? _a : null;
        const lastFrameOmitted = (_b = framesOmitted === null || framesOmitted === void 0 ? void 0 : framesOmitted[1]) !== null && _b !== void 0 ? _b : null;
        const lastFrameIndex = getLastFrameIndex();
        let nRepeats = 0;
        const maxLengthOfAllRelativeAddresses = frames.reduce((maxLengthUntilThisPoint, frame) => {
            const correspondingImage = findImageForAddress(frame.instructionAddr, frame.addrMode);
            try {
                const relativeAddress = ((0, utils_1.parseAddress)(frame.instructionAddr) -
                    (0, utils_1.parseAddress)(correspondingImage.image_addr)).toString(16);
                return maxLengthUntilThisPoint > relativeAddress.length
                    ? maxLengthUntilThisPoint
                    : relativeAddress.length;
            }
            catch (_a) {
                return maxLengthUntilThisPoint;
            }
        }, 0);
        const convertedFrames = frames
            .map((frame, frameIndex) => {
            const prevFrame = frames[frameIndex - 1];
            const nextFrame = frames[frameIndex + 1];
            const repeatedFrame = nextFrame &&
                frame.lineNo === nextFrame.lineNo &&
                frame.instructionAddr === nextFrame.instructionAddr &&
                frame.package === nextFrame.package &&
                frame.module === nextFrame.module &&
                frame.function === nextFrame.function;
            if (repeatedFrame) {
                nRepeats++;
            }
            const isUsedForGrouping = isFrameUsedForGrouping(frame);
            const isVisible = includeSystemFrames ||
                frame.inApp ||
                (nextFrame && nextFrame.inApp) ||
                // the last non-app frame
                (!frame.inApp && !nextFrame) ||
                isUsedForGrouping;
            if (isVisible && !repeatedFrame) {
                const lineProps = {
                    event,
                    frame,
                    prevFrame,
                    nextFrame,
                    isExpanded: expandFirstFrame && lastFrameIndex === frameIndex,
                    emptySourceNotation: lastFrameIndex === frameIndex && frameIndex === 0,
                    platform,
                    timesRepeated: nRepeats,
                    showingAbsoluteAddress: showingAbsoluteAddresses,
                    onAddressToggle: handleToggleAddresses,
                    image: findImageForAddress(frame.instructionAddr, frame.addrMode),
                    maxLengthOfRelativeAddress: maxLengthOfAllRelativeAddresses,
                    registers: {},
                    includeSystemFrames,
                    onFunctionNameToggle: handleToggleFunctionName,
                    showCompleteFunctionName,
                    isHoverPreviewed,
                    isUsedForGrouping,
                };
                nRepeats = 0;
                if (frameIndex === firstFrameOmitted) {
                    return (<react_1.Fragment key={frameIndex}>
                <lineV2_1.default {...lineProps}/>
                {renderOmittedFrames(firstFrameOmitted, lastFrameOmitted)}
              </react_1.Fragment>);
                }
                return <lineV2_1.default key={frameIndex} {...lineProps}/>;
            }
            if (!repeatedFrame) {
                nRepeats = 0;
            }
            if (frameIndex !== firstFrameOmitted) {
                return null;
            }
            return renderOmittedFrames(firstFrameOmitted, lastFrameOmitted);
        })
            .filter(frame => !!frame);
        if (convertedFrames.length > 0 && registers) {
            const lastFrame = convertedFrames.length - 1;
            convertedFrames[lastFrame] = (0, react_1.cloneElement)(convertedFrames[lastFrame], {
                registers,
            });
            if (!newestFirst) {
                return convertedFrames;
            }
            return [...convertedFrames].reverse();
        }
        if (!newestFirst) {
            return convertedFrames;
        }
        return [...convertedFrames].reverse();
    }
    return (<Wrapper className={getClassName()}>
      <StyledPlatformIcon platform={(0, utils_1.stackTracePlatformIcon)(platform, frames)} size="20px" style={{ borderRadius: '3px 0 0 3px' }}/>
      <StyledList>{renderConvertedFrames()}</StyledList>
    </Wrapper>);
}
exports.default = StackTraceContent;
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  position: absolute;
  margin-top: -1px;
  left: -${(0, space_1.default)(3)};
`;
const StyledList = (0, styled_1.default)(list_1.default) `
  grid-gap: 0;
`;
//# sourceMappingURL=stacktraceContentV2.jsx.map