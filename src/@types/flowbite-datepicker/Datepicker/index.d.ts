//  create me declaration file for flowbite-datepicker class Datepicker
declare module 'flowbite-datepicker/Datepicker' {
    export default class Datepicker {
        constructor(element: HTMLElement, options?: Partial<DatepickerOptions>)

        // static methods
        static attachTo(element: HTMLElement, options?: Partial<DatepickerOptions>): Datepicker

        // public methods
        destroy(): void
        setDate(date: Date): void
        getOptions(): DatepickerOptions
        getValue(): string
        hide(): void
        setOptions(options: Partial<DatepickerOptions>): void
        setValue(value: string): void
        show(): void
    }
}

//create interface for DatepickerOptions
interface DatepickerOptions {
    // properties
    autohide?: boolean
    buttonClass?: string
    buttonLabel?: string
    buttonOnly?: boolean
    buttonPosition?: string
    buttonWrapperClass?: string
    calendarClass?: string
    calendarWrapperClass?: string
    clearButton?: boolean
    clearButtonLabel?: string
    clearButtonWrapperClass?: string
    dateDelimiter?: string
    dateFormat?: string
    dateInputClass?: string
    dateInputPlaceholder?: string
    dateInputWrapperClass?: string
    days?: string[]
    minDate: Date
    todayHighlight: boolean
}
