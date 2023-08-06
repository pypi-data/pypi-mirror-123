Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_select_1 = (0, tslib_1.__importStar)(require("react-select"));
const async_1 = (0, tslib_1.__importDefault)(require("react-select/async"));
const async_creatable_1 = (0, tslib_1.__importDefault)(require("react-select/async-creatable"));
const creatable_1 = (0, tslib_1.__importDefault)(require("react-select/creatable"));
const react_1 = require("@emotion/react");
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const icons_1 = require("app/icons");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const convertFromSelect2Choices_1 = (0, tslib_1.__importDefault)(require("app/utils/convertFromSelect2Choices"));
function isGroupedOptions(maybe) {
    if (!maybe || maybe.length === 0) {
        return false;
    }
    return maybe[0].options !== undefined;
}
const ClearIndicator = (props) => (<react_select_1.components.ClearIndicator {...props}>
    <icons_1.IconClose size="10px"/>
  </react_select_1.components.ClearIndicator>);
const DropdownIndicator = (props) => (<react_select_1.components.DropdownIndicator {...props}>
    <icons_1.IconChevron direction="down" size="14px"/>
  </react_select_1.components.DropdownIndicator>);
const MultiValueRemove = (props) => (<react_select_1.components.MultiValueRemove {...props}>
    <icons_1.IconClose size="8px"/>
  </react_select_1.components.MultiValueRemove>);
const SelectLoadingIndicator = () => (<loadingIndicator_1.default mini size={20} style={{ height: 20, width: 20 }}/>);
function SelectControl(props) {
    const theme = (0, react_1.useTheme)();
    // TODO(epurkhiser): The loading indicator should probably also be our loading
    // indicator.
    // Unfortunately we cannot use emotions `css` helper here, since react-select
    // *requires* object styles, which the css helper cannot produce.
    const indicatorStyles = (_a) => {
        var { padding: _padding } = _a, provided = (0, tslib_1.__rest)(_a, ["padding"]);
        return (Object.assign(Object.assign({}, provided), { padding: '4px', alignItems: 'center', cursor: 'pointer', color: theme.subText }));
    };
    const defaultStyles = {
        control: (_, state) => (Object.assign(Object.assign(Object.assign(Object.assign(Object.assign(Object.assign({ height: '100%', fontSize: theme.fontSizeLarge, lineHeight: theme.text.lineHeightBody, display: 'flex' }, {
            color: theme.formText,
            background: theme.background,
            border: `1px solid ${theme.border}`,
            boxShadow: `inset ${theme.dropShadowLight}`,
        }), { borderRadius: theme.borderRadius, transition: 'border 0.1s linear', alignItems: 'center', minHeight: '40px', '&:hover': {
                borderColor: theme.border,
            } }), (state.isFocused && {
            border: `1px solid ${theme.border}`,
            boxShadow: 'rgba(209, 202, 216, 0.5) 0 0 0 3px',
        })), (state.menuIsOpen && {
            borderBottomLeftRadius: '0',
            borderBottomRightRadius: '0',
            boxShadow: 'none',
        })), (state.isDisabled && {
            borderColor: theme.border,
            background: theme.backgroundSecondary,
            color: theme.disabled,
            cursor: 'not-allowed',
        })), (!state.isSearchable && {
            cursor: 'pointer',
        }))),
        menu: (provided) => (Object.assign(Object.assign({}, provided), { zIndex: theme.zIndex.dropdown, marginTop: '-1px', background: theme.background, border: `1px solid ${theme.border}`, borderRadius: `0 0 ${theme.borderRadius} ${theme.borderRadius}`, borderTop: `1px solid ${theme.border}`, boxShadow: theme.dropShadowLight })),
        option: (provided, state) => (Object.assign(Object.assign({}, provided), { lineHeight: '1.5', fontSize: theme.fontSizeMedium, cursor: 'pointer', color: state.isFocused
                ? theme.textColor
                : state.isSelected
                    ? theme.background
                    : theme.textColor, backgroundColor: state.isFocused
                ? theme.focus
                : state.isSelected
                    ? theme.active
                    : 'transparent', '&:active': {
                backgroundColor: theme.active,
            } })),
        valueContainer: (provided) => (Object.assign(Object.assign({}, provided), { alignItems: 'center' })),
        input: (provided) => (Object.assign(Object.assign({}, provided), { color: theme.formText })),
        singleValue: (provided) => (Object.assign(Object.assign({}, provided), { color: theme.formText })),
        placeholder: (provided) => (Object.assign(Object.assign({}, provided), { color: theme.formPlaceholder })),
        multiValue: (provided) => (Object.assign(Object.assign({}, provided), { color: '#007eff', backgroundColor: '#ebf5ff', borderRadius: '2px', border: '1px solid #c2e0ff', display: 'flex' })),
        multiValueLabel: (provided) => (Object.assign(Object.assign({}, provided), { color: '#007eff', padding: '0', paddingLeft: '6px', lineHeight: '1.8' })),
        multiValueRemove: () => ({
            cursor: 'pointer',
            alignItems: 'center',
            borderLeft: '1px solid #c2e0ff',
            borderRadius: '0 2px 2px 0',
            display: 'flex',
            padding: '0 4px',
            marginLeft: '4px',
            '&:hover': {
                color: '#6284b9',
                background: '#cce5ff',
            },
        }),
        indicatorsContainer: () => ({
            display: 'grid',
            gridAutoFlow: 'column',
            gridGap: '2px',
            marginRight: '6px',
        }),
        clearIndicator: indicatorStyles,
        dropdownIndicator: indicatorStyles,
        loadingIndicator: indicatorStyles,
        groupHeading: (provided) => (Object.assign(Object.assign({}, provided), { lineHeight: '1.5', fontWeight: 600, backgroundColor: theme.backgroundSecondary, color: theme.textColor, marginBottom: 0, padding: `${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)}` })),
        group: (provided) => (Object.assign(Object.assign({}, provided), { padding: 0 })),
    };
    const getFieldLabelStyle = (label) => ({
        ':before': {
            content: `"${label}"`,
            color: theme.gray300,
            fontWeight: 600,
        },
    });
    const { async, creatable, options, choices, clearable, components, styles, value, inFieldLabel } = props, rest = (0, tslib_1.__rest)(props, ["async", "creatable", "options", "choices", "clearable", "components", "styles", "value", "inFieldLabel"]);
    // Compatibility with old select2 API
    const choicesOrOptions = (0, convertFromSelect2Choices_1.default)(typeof choices === 'function' ? choices(props) : choices) ||
        options;
    // It's possible that `choicesOrOptions` does not exist (e.g. in the case of AsyncSelect)
    let mappedValue = value;
    if (choicesOrOptions) {
        /**
         * Value is expected to be object like the options list, we map it back from the options list.
         * Note that if the component doesn't have options or choices passed in
         * because the select component fetches the options finding the mappedValue will fail
         * and the component won't work
         */
        let flatOptions = [];
        if (isGroupedOptions(choicesOrOptions)) {
            flatOptions = choicesOrOptions.flatMap(option => option.options);
        }
        else {
            // @ts-ignore The types used in react-select generics (OptionType) don't
            // line up well with our option type (SelectValue). We need to do more work
            // to get these types to align.
            flatOptions = choicesOrOptions.flatMap(option => option);
        }
        mappedValue =
            props.multiple && Array.isArray(value)
                ? value.map(val => flatOptions.find(option => option.value === val))
                : flatOptions.find(opt => opt.value === value) || value;
    }
    // Override the default style with in-field labels if they are provided
    const inFieldLabelStyles = {
        singleValue: (base) => (Object.assign(Object.assign({}, base), getFieldLabelStyle(inFieldLabel))),
        placeholder: (base) => (Object.assign(Object.assign({}, base), getFieldLabelStyle(inFieldLabel))),
    };
    const labelOrDefaultStyles = inFieldLabel
        ? (0, react_select_1.mergeStyles)(defaultStyles, inFieldLabelStyles)
        : defaultStyles;
    // Allow the provided `styles` prop to override default styles using the same
    // function interface provided by react-styled. This ensures the `provided`
    // styles include our overridden default styles
    const mappedStyles = styles
        ? (0, react_select_1.mergeStyles)(labelOrDefaultStyles, styles)
        : labelOrDefaultStyles;
    const replacedComponents = {
        ClearIndicator,
        DropdownIndicator,
        MultiValueRemove,
        LoadingIndicator: SelectLoadingIndicator,
        IndicatorSeparator: null,
    };
    return (<SelectPicker styles={mappedStyles} components={Object.assign(Object.assign({}, replacedComponents), components)} async={async} creatable={creatable} isClearable={clearable} backspaceRemovesValue={clearable} value={mappedValue} isMulti={props.multiple || props.multi} isDisabled={props.isDisabled || props.disabled} options={options || choicesOrOptions} openMenuOnFocus={props.openMenuOnFocus === undefined ? true : props.openMenuOnFocus} {...rest}/>);
}
function SelectPicker(_a) {
    var { async, creatable, forwardedRef } = _a, props = (0, tslib_1.__rest)(_a, ["async", "creatable", "forwardedRef"]);
    // Pick the right component to use
    // Using any here as react-select types also use any
    let Component;
    if (async && creatable) {
        Component = async_creatable_1.default;
    }
    else if (async && !creatable) {
        Component = async_1.default;
    }
    else if (creatable) {
        Component = creatable_1.default;
    }
    else {
        Component = react_select_1.default;
    }
    return <Component ref={forwardedRef} {...props}/>;
}
// The generics need to be filled here as forwardRef can't expose generics.
const RefForwardedSelectControl = React.forwardRef(function RefForwardedSelectControl(props, ref) {
    return <SelectControl forwardedRef={ref} {...props}/>;
});
exports.default = RefForwardedSelectControl;
//# sourceMappingURL=selectControl.jsx.map