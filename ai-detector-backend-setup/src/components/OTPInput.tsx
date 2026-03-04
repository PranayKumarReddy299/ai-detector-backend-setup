import React, { useState, useRef, useEffect } from 'react';

interface OTPInputProps {
  length?: number;
  value: string;
  onChange: (value: string) => void;
  disabled?: boolean;
}

const OTPInput: React.FC<OTPInputProps> = ({ length = 6, value, onChange, disabled = false }) => {
  const [otp, setOtp] = useState<string[]>(value.split('').concat(Array(length - value.length).fill('')));
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  useEffect(() => {
    const newOtp = value.split('').concat(Array(length - value.length).fill(''));
    setOtp(newOtp.slice(0, length));
  }, [value, length]);

  const handleChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value;
    
    if (val.length > 1) {
      // Handle paste
      const pastedValue = val.slice(0, length);
      const newOtp = pastedValue.split('').concat(Array(length - pastedValue.length).fill(''));
      setOtp(newOtp);
      onChange(pastedValue);
      if (pastedValue.length === length) {
        inputRefs.current[length - 1]?.focus();
      } else {
        inputRefs.current[pastedValue.length]?.focus();
      }
      return;
    }

    if (!/^\d*$/.test(val)) return;

    const newOtp = [...otp];
    newOtp[index] = val;
    setOtp(newOtp);
    onChange(newOtp.join(''));

    if (val && index < length - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !otp[index] && index > 0) {
      inputRefs.current[index - 1]?.focus();
    }
  };

  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, length);
    const newOtp = pastedData.split('').concat(Array(length - pastedData.length).fill(''));
    setOtp(newOtp);
    onChange(pastedData);
    inputRefs.current[Math.min(pastedData.length, length - 1)]?.focus();
  };

  return (
    <div className="flex justify-center gap-2 sm:gap-3">
      {otp.map((digit, index) => (
        <input
          key={index}
          ref={(ref) => { inputRefs.current[index] = ref; }}
          type="text"
          inputMode="numeric"
          maxLength={6}
          value={digit}
          onChange={(e) => handleChange(index, e)}
          onKeyDown={(e) => handleKeyDown(index, e)}
          onPaste={handlePaste}
          disabled={disabled}
          className={`w-10 h-12 sm:w-12 sm:h-14 text-center text-xl font-bold border-2 rounded-lg 
            focus:outline-none focus:ring-2 focus:ring-green-500 focus:border-green-500
            transition-all duration-200
            ${disabled ? 'bg-gray-100 cursor-not-allowed' : 'bg-white hover:border-green-400'}
            ${digit ? 'border-green-500 bg-green-50' : 'border-gray-300'}`}
        />
      ))}
    </div>
  );
};

export default OTPInput;
