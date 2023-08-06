Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const platformicons_1 = require("platformicons");
const line_1 = (0, tslib_1.__importDefault)(require("app/components/events/interfaces/frame/line"));
const utils_1 = require("app/components/events/interfaces/utils");
const locale_1 = require("app/locale");
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const defaultProps = {
    includeSystemFrames: true,
    expandFirstFrame: true,
};
class StacktraceContent extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            showingAbsoluteAddresses: false,
            showCompleteFunctionName: false,
        };
        this.renderOmittedFrames = (firstFrameOmitted, lastFrameOmitted) => {
            const props = {
                className: 'frame frames-omitted',
                key: 'omitted',
            };
            const text = (0, locale_1.t)('Frames %d until %d were omitted and not available.', firstFrameOmitted, lastFrameOmitted);
            return <li {...props}>{text}</li>;
        };
        this.frameIsVisible = (frame, nextFrame) => {
            const { includeSystemFrames } = this.props;
            return (includeSystemFrames ||
                frame.inApp ||
                (nextFrame && nextFrame.inApp) ||
                // the last non-app frame
                (!frame.inApp && !nextFrame));
        };
        this.handleToggleAddresses = (event) => {
            event.stopPropagation(); // to prevent collapsing if collapsible
            this.setState(prevState => ({
                showingAbsoluteAddresses: !prevState.showingAbsoluteAddresses,
            }));
        };
        this.handleToggleFunctionName = (event) => {
            event.stopPropagation(); // to prevent collapsing if collapsible
            this.setState(prevState => ({
                showCompleteFunctionName: !prevState.showCompleteFunctionName,
            }));
        };
    }
    isFrameAfterLastNonApp() {
        var _a;
        const { data } = this.props;
        const frames = (_a = data.frames) !== null && _a !== void 0 ? _a : [];
        if (!frames.length || frames.length < 2) {
            return false;
        }
        const lastFrame = frames[frames.length - 1];
        const penultimateFrame = frames[frames.length - 2];
        return penultimateFrame.inApp && !lastFrame.inApp;
    }
    findImageForAddress(address, addrMode) {
        var _a, _b;
        const images = (_b = (_a = this.props.event.entries.find(entry => entry.type === 'debugmeta')) === null || _a === void 0 ? void 0 : _a.data) === null || _b === void 0 ? void 0 : _b.images;
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
    getClassName() {
        const { className = '', includeSystemFrames } = this.props;
        if (includeSystemFrames) {
            return `${className} traceback full-traceback`;
        }
        return `${className} traceback in-app-traceback`;
    }
    render() {
        var _a, _b, _c, _d, _e;
        const { data, event, newestFirst, expandFirstFrame, platform, includeSystemFrames, isHoverPreviewed, } = this.props;
        const { showingAbsoluteAddresses, showCompleteFunctionName } = this.state;
        let firstFrameOmitted = null;
        let lastFrameOmitted = null;
        if (data.framesOmitted) {
            firstFrameOmitted = data.framesOmitted[0];
            lastFrameOmitted = data.framesOmitted[1];
        }
        let lastFrameIdx = null;
        ((_a = data.frames) !== null && _a !== void 0 ? _a : []).forEach((frame, frameIdx) => {
            if (frame.inApp) {
                lastFrameIdx = frameIdx;
            }
        });
        if (lastFrameIdx === null) {
            lastFrameIdx = ((_b = data.frames) !== null && _b !== void 0 ? _b : []).length - 1;
        }
        const frames = [];
        let nRepeats = 0;
        const maxLengthOfAllRelativeAddresses = ((_c = data.frames) !== null && _c !== void 0 ? _c : []).reduce((maxLengthUntilThisPoint, frame) => {
            const correspondingImage = this.findImageForAddress(frame.instructionAddr, frame.addrMode);
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
        const isFrameAfterLastNonApp = this.isFrameAfterLastNonApp();
        ((_d = data.frames) !== null && _d !== void 0 ? _d : []).forEach((frame, frameIdx) => {
            var _a, _b, _c;
            const prevFrame = ((_a = data.frames) !== null && _a !== void 0 ? _a : [])[frameIdx - 1];
            const nextFrame = ((_b = data.frames) !== null && _b !== void 0 ? _b : [])[frameIdx + 1];
            const repeatedFrame = nextFrame &&
                frame.lineNo === nextFrame.lineNo &&
                frame.instructionAddr === nextFrame.instructionAddr &&
                frame.package === nextFrame.package &&
                frame.module === nextFrame.module &&
                frame.function === nextFrame.function;
            if (repeatedFrame) {
                nRepeats++;
            }
            if (this.frameIsVisible(frame, nextFrame) && !repeatedFrame) {
                const image = this.findImageForAddress(frame.instructionAddr, frame.addrMode);
                frames.push(<line_1.default key={frameIdx} event={event} data={frame} isExpanded={expandFirstFrame && lastFrameIdx === frameIdx} emptySourceNotation={lastFrameIdx === frameIdx && frameIdx === 0} isOnlyFrame={((_c = data.frames) !== null && _c !== void 0 ? _c : []).length === 1} nextFrame={nextFrame} prevFrame={prevFrame} platform={platform} timesRepeated={nRepeats} showingAbsoluteAddress={showingAbsoluteAddresses} onAddressToggle={this.handleToggleAddresses} image={image} maxLengthOfRelativeAddress={maxLengthOfAllRelativeAddresses} registers={{}} // TODO: Fix registers
                 isFrameAfterLastNonApp={isFrameAfterLastNonApp} includeSystemFrames={includeSystemFrames} onFunctionNameToggle={this.handleToggleFunctionName} showCompleteFunctionName={showCompleteFunctionName} isHoverPreviewed={isHoverPreviewed} isFirst={newestFirst ? frameIdx === lastFrameIdx : frameIdx === 0}/>);
            }
            if (!repeatedFrame) {
                nRepeats = 0;
            }
            if (frameIdx === firstFrameOmitted) {
                frames.push(this.renderOmittedFrames(firstFrameOmitted, lastFrameOmitted));
            }
        });
        if (frames.length > 0 && data.registers) {
            const lastFrame = frames.length - 1;
            frames[lastFrame] = React.cloneElement(frames[lastFrame], {
                registers: data.registers,
            });
        }
        if (newestFirst) {
            frames.reverse();
        }
        const className = this.getClassName();
        const platformIcon = (0, utils_1.stackTracePlatformIcon)(platform, (_e = data.frames) !== null && _e !== void 0 ? _e : []);
        return (<Wrapper className={className} data-test-id="stack-trace-content">
        <StyledPlatformIcon platform={platformIcon} size="20px" style={{ borderRadius: '3px 0 0 3px' }} data-test-id={`platform-icon-${platformIcon}`}/>
        <StyledList data-test-id="frames">{frames}</StyledList>
      </Wrapper>);
    }
}
StacktraceContent.defaultProps = {
    includeSystemFrames: true,
    expandFirstFrame: true,
};
exports.default = (0, withOrganization_1.default)(StacktraceContent);
const Wrapper = (0, styled_1.default)('div') `
  position: relative;
`;
const StyledPlatformIcon = (0, styled_1.default)(platformicons_1.PlatformIcon) `
  position: absolute;
  top: -1px;
  left: -20px;
`;
const StyledList = (0, styled_1.default)('ul') `
  list-style: none;
`;
//# sourceMappingURL=stacktraceContent.jsx.map