Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const indicator_1 = require("app/actionCreators/indicator");
const well_1 = (0, tslib_1.__importDefault)(require("app/components/well"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const resizerPositions = {
    nw: ['top', 'left'],
    ne: ['top', 'right'],
    se: ['bottom', 'right'],
    sw: ['bottom', 'left'],
};
class AvatarCropper extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            file: null,
            objectURL: null,
            mousePosition: { pageX: 0, pageY: 0 },
            resizeDimensions: { top: 0, left: 0, size: 0 },
            resizeDirection: null,
        };
        this.file = React.createRef();
        this.canvas = React.createRef();
        this.image = React.createRef();
        this.cropContainer = React.createRef();
        // These values must be synced with the avatar endpoint in backend.
        this.MIN_DIMENSION = 256;
        this.MAX_DIMENSION = 1024;
        this.ALLOWED_MIMETYPES = 'image/gif,image/jpeg,image/png';
        this.onSelectFile = (ev) => {
            const file = ev.target.files && ev.target.files[0];
            // No file selected (e.g. user clicked "cancel")
            if (!file) {
                return;
            }
            if (!/^image\//.test(file.type)) {
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('That is not a supported file type.'));
                return;
            }
            this.revokeObjectUrl();
            const { updateDataUrlState } = this.props;
            const objectURL = window.URL.createObjectURL(file);
            this.setState({ file, objectURL }, () => updateDataUrlState({ savedDataUrl: null }));
        };
        this.revokeObjectUrl = () => this.state.objectURL && window.URL.revokeObjectURL(this.state.objectURL);
        this.onImageLoad = () => {
            const error = this.validateImage();
            if (error) {
                this.revokeObjectUrl();
                this.setState({ objectURL: null });
                (0, indicator_1.addErrorMessage)(error);
                return;
            }
            const image = this.image.current;
            if (!image) {
                return;
            }
            const dimension = Math.min(image.clientHeight, image.clientWidth);
            const state = { resizeDimensions: { size: dimension, top: 0, left: 0 } };
            this.setState(state, this.drawToCanvas);
        };
        this.updateDimensions = (ev) => {
            const cropContainer = this.cropContainer.current;
            if (!cropContainer) {
                return;
            }
            const { mousePosition, resizeDimensions } = this.state;
            let pageY = ev.pageY;
            let pageX = ev.pageX;
            let top = resizeDimensions.top + (pageY - mousePosition.pageY);
            let left = resizeDimensions.left + (pageX - mousePosition.pageX);
            if (top < 0) {
                top = 0;
                pageY = mousePosition.pageY;
            }
            else if (top + resizeDimensions.size > cropContainer.clientHeight) {
                top = cropContainer.clientHeight - resizeDimensions.size;
                pageY = mousePosition.pageY;
            }
            if (left < 0) {
                left = 0;
                pageX = mousePosition.pageX;
            }
            else if (left + resizeDimensions.size > cropContainer.clientWidth) {
                left = cropContainer.clientWidth - resizeDimensions.size;
                pageX = mousePosition.pageX;
            }
            this.setState(state => ({
                resizeDimensions: Object.assign(Object.assign({}, state.resizeDimensions), { top, left }),
                mousePosition: { pageX, pageY },
            }));
        };
        this.onMouseDown = (ev) => {
            ev.preventDefault();
            this.setState({ mousePosition: { pageY: ev.pageY, pageX: ev.pageX } });
            document.addEventListener('mousemove', this.updateDimensions);
            document.addEventListener('mouseup', this.onMouseUp);
        };
        this.onMouseUp = (ev) => {
            ev.preventDefault();
            document.removeEventListener('mousemove', this.updateDimensions);
            document.removeEventListener('mouseup', this.onMouseUp);
            this.drawToCanvas();
        };
        this.startResize = (direction, ev) => {
            ev.stopPropagation();
            ev.preventDefault();
            document.addEventListener('mousemove', this.updateSize);
            document.addEventListener('mouseup', this.stopResize);
            this.setState({
                resizeDirection: direction,
                mousePosition: { pageY: ev.pageY, pageX: ev.pageX },
            });
        };
        this.stopResize = (ev) => {
            ev.stopPropagation();
            ev.preventDefault();
            document.removeEventListener('mousemove', this.updateSize);
            document.removeEventListener('mouseup', this.stopResize);
            this.setState({ resizeDirection: null });
            this.drawToCanvas();
        };
        this.updateSize = (ev) => {
            const cropContainer = this.cropContainer.current;
            if (!cropContainer) {
                return;
            }
            const { mousePosition } = this.state;
            const yDiff = ev.pageY - mousePosition.pageY;
            const xDiff = ev.pageX - mousePosition.pageX;
            this.setState({
                resizeDimensions: this.getNewDimensions(cropContainer, yDiff, xDiff),
                mousePosition: { pageX: ev.pageX, pageY: ev.pageY },
            });
        };
        // Normalize diff across dimensions so that negative diffs are always making
        // the cropper smaller and positive ones are making the cropper larger
        this.getDiffNW = (yDiff, xDiff) => (yDiff - yDiff * 2 + (xDiff - xDiff * 2)) / 2;
        this.getDiffNE = (yDiff, xDiff) => (yDiff - yDiff * 2 + xDiff) / 2;
        this.getDiffSW = (yDiff, xDiff) => (yDiff + (xDiff - xDiff * 2)) / 2;
        this.getDiffSE = (yDiff, xDiff) => (yDiff + xDiff) / 2;
        this.getNewDimensions = (container, yDiff, xDiff) => {
            const { resizeDimensions: oldDimensions, resizeDirection } = this.state;
            const diff = this['getDiff' + resizeDirection.toUpperCase()](yDiff, xDiff);
            let height = container.clientHeight - oldDimensions.top;
            let width = container.clientWidth - oldDimensions.left;
            // Depending on the direction, we update different dimensions:
            // nw: size, top, left
            // ne: size, top
            // sw: size, left
            // se: size
            const editingTop = resizeDirection === 'nw' || resizeDirection === 'ne';
            const editingLeft = resizeDirection === 'nw' || resizeDirection === 'sw';
            const newDimensions = {
                top: 0,
                left: 0,
                size: oldDimensions.size + diff,
            };
            if (editingTop) {
                newDimensions.top = oldDimensions.top - diff;
                height = container.clientHeight - newDimensions.top;
            }
            if (editingLeft) {
                newDimensions.left = oldDimensions.left - diff;
                width = container.clientWidth - newDimensions.left;
            }
            if (newDimensions.top < 0) {
                newDimensions.size = newDimensions.size + newDimensions.top;
                if (editingLeft) {
                    newDimensions.left = newDimensions.left - newDimensions.top;
                }
                newDimensions.top = 0;
            }
            if (newDimensions.left < 0) {
                newDimensions.size = newDimensions.size + newDimensions.left;
                if (editingTop) {
                    newDimensions.top = newDimensions.top - newDimensions.left;
                }
                newDimensions.left = 0;
            }
            const maxSize = Math.min(width, height);
            if (newDimensions.size > maxSize) {
                if (editingTop) {
                    newDimensions.top = newDimensions.top + newDimensions.size - maxSize;
                }
                if (editingLeft) {
                    newDimensions.left = newDimensions.left + newDimensions.size - maxSize;
                }
                newDimensions.size = maxSize;
            }
            else if (newDimensions.size < this.MIN_DIMENSION) {
                if (editingTop) {
                    newDimensions.top = newDimensions.top + newDimensions.size - this.MIN_DIMENSION;
                }
                if (editingLeft) {
                    newDimensions.left = newDimensions.left + newDimensions.size - this.MIN_DIMENSION;
                }
                newDimensions.size = this.MIN_DIMENSION;
            }
            return Object.assign(Object.assign({}, oldDimensions), newDimensions);
        };
        this.uploadClick = (ev) => {
            ev.preventDefault();
            this.file.current && this.file.current.click();
        };
    }
    componentWillUnmount() {
        this.revokeObjectUrl();
    }
    validateImage() {
        const img = this.image.current;
        if (!img) {
            return null;
        }
        if (img.naturalWidth < this.MIN_DIMENSION || img.naturalHeight < this.MIN_DIMENSION) {
            return (0, locale_1.tct)('Please upload an image larger than [size]px by [size]px.', {
                size: this.MIN_DIMENSION - 1,
            });
        }
        if (img.naturalWidth > this.MAX_DIMENSION || img.naturalHeight > this.MAX_DIMENSION) {
            return (0, locale_1.tct)('Please upload an image smaller than [size]px by [size]px.', {
                size: this.MAX_DIMENSION,
            });
        }
        return null;
    }
    drawToCanvas() {
        const canvas = this.canvas.current;
        if (!canvas) {
            return;
        }
        const image = this.image.current;
        if (!image) {
            return;
        }
        const { left, top, size } = this.state.resizeDimensions;
        // Calculate difference between natural dimensions and rendered dimensions
        const ratio = (image.naturalHeight / image.clientHeight +
            image.naturalWidth / image.clientWidth) /
            2;
        canvas.width = size * ratio;
        canvas.height = size * ratio;
        canvas
            .getContext('2d')
            .drawImage(image, left * ratio, top * ratio, size * ratio, size * ratio, 0, 0, size * ratio, size * ratio);
        this.props.updateDataUrlState({ dataUrl: canvas.toDataURL() });
    }
    get imageSrc() {
        var _a;
        const { savedDataUrl, model, type } = this.props;
        const uuid = (_a = model.avatar) === null || _a === void 0 ? void 0 : _a.avatarUuid;
        const photoUrl = uuid && `/${constants_1.AVATAR_URL_MAP[type] || 'avatar'}/${uuid}/`;
        return savedDataUrl || this.state.objectURL || photoUrl;
    }
    renderImageCrop() {
        const src = this.imageSrc;
        if (!src) {
            return null;
        }
        const { resizeDimensions, resizeDirection } = this.state;
        const style = {
            top: resizeDimensions.top,
            left: resizeDimensions.left,
            width: resizeDimensions.size,
            height: resizeDimensions.size,
        };
        return (<ImageCropper resizeDirection={resizeDirection}>
        <CropContainer ref={this.cropContainer}>
          <img ref={this.image} src={src} onLoad={this.onImageLoad} onDragStart={e => e.preventDefault()}/>
          <Cropper style={style} onMouseDown={this.onMouseDown}>
            {Object.keys(resizerPositions).map(pos => (<Resizer key={pos} position={pos} onMouseDown={this.startResize.bind(this, pos)}/>))}
          </Cropper>
        </CropContainer>
      </ImageCropper>);
    }
    render() {
        const src = this.imageSrc;
        const upload = <a onClick={this.uploadClick}/>;
        const uploader = (<well_1.default hasImage centered>
        <p>{(0, locale_1.tct)('[upload:Upload a photo] to get started.', { upload })}</p>
      </well_1.default>);
        return (<React.Fragment>
        {!src && uploader}
        {src && <HiddenCanvas ref={this.canvas}/>}
        {this.renderImageCrop()}
        <div className="form-group">
          {src && <a onClick={this.uploadClick}>{(0, locale_1.t)('Change Photo')}</a>}
          <UploadInput ref={this.file} type="file" accept={this.ALLOWED_MIMETYPES} onChange={this.onSelectFile}/>
        </div>
      </React.Fragment>);
    }
}
exports.default = AvatarCropper;
const UploadInput = (0, styled_1.default)('input') `
  position: absolute;
  opacity: 0;
`;
const ImageCropper = (0, styled_1.default)('div') `
  cursor: ${p => (p.resizeDirection ? `${p.resizeDirection}-resize` : 'default')};
  text-align: center;
  margin-bottom: 20px;
  background-size: 20px 20px;
  background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
  background-color: ${p => p.theme.background};
  background-image: linear-gradient(
      45deg,
      ${p => p.theme.backgroundSecondary} 25%,
      rgba(0, 0, 0, 0) 25%
    ),
    linear-gradient(-45deg, ${p => p.theme.backgroundSecondary} 25%, rgba(0, 0, 0, 0) 25%),
    linear-gradient(45deg, rgba(0, 0, 0, 0) 75%, ${p => p.theme.backgroundSecondary} 75%),
    linear-gradient(-45deg, rgba(0, 0, 0, 0) 75%, ${p => p.theme.backgroundSecondary} 75%);
`;
const CropContainer = (0, styled_1.default)('div') `
  display: inline-block;
  position: relative;
  max-width: 100%;
`;
const Cropper = (0, styled_1.default)('div') `
  position: absolute;
  border: 2px dashed ${p => p.theme.gray300};
`;
const Resizer = (0, styled_1.default)('div') `
  border-radius: 5px;
  width: 10px;
  height: 10px;
  position: absolute;
  background-color: ${p => p.theme.gray300};
  cursor: ${p => `${p.position}-resize`};
  ${p => resizerPositions[p.position].map(pos => `${pos}: -5px;`)}
`;
const HiddenCanvas = (0, styled_1.default)('canvas') `
  display: none;
`;
//# sourceMappingURL=avatarCropper.jsx.map