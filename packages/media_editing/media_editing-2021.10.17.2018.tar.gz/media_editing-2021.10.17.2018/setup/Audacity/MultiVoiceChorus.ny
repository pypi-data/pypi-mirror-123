;nyquist plug-in
;version 3
;type process
;categories "http://lv2plug.in/ns/lv2core/#ChorusPlugin"
;name "Multi-Voice Chorus..."
;action "Applying multi-voice chorus..."
;info "by Steve Daulton (www.easyspacepro.com).\nReleased under GPL v2.\n"

;; MultiVoiceChorus.ny by Steve Daulton Sept 2012
;; Released under terms of the GNU General Public License version 2:
;; http://www.gnu.org/licenses/old-licenses/gpl-2.0.html 
;;
;; For information about writing and modifying Nyquist plug-ins:
;; http://wiki.audacityteam.org/wiki/Nyquist_Plug-ins_Reference

;control rate "Speed" real "" 5 0 10
;control depth "Depth" real "" 5 0 10
;control voices "Voices" int "" 2 1 4
;control mix "Mix" real "" 5 0 10
;control limiter "Output Limiter" choice "Disabled,Enabled" 1 

(setq depth (max 0 (* 0.00001 (power depth 3.0))))
(setq rate (max 0 (* 0.005 (power rate 3.0))))
(setq voices (max 1 voices))
(setq mix (max 0 mix))

;;; brick wall limiter
(defun limit (s-in &optional (hld 7.0)) 
  (let* ((la-time (/ hld 3000.0))                 ; lookahead time (seconds)
         (la-s (round (* la-time *sound-srate*))) ; lookahead samples
         (pad-time (* 3 la-time))                 ; padding required at start (s)
         (pad-s (* 3 la-s))                       ; padding smaples
         (padding (snd-const (peak s-in pad-s) 0 *sound-srate* (* 3.0 la-time)))
         (peak-env (snd-avg s-in (* 4 la-s) la-s OP-PEAK))
         (peak-env (sim padding (at-abs pad-time (cue peak-env))))
         (peak-env (extract 0 1 (s-max 1 peak-env))))
    (mult s-in 0.999
      (snd-exp 
        (mult -1 (snd-log peak-env))))))

;;; multi-voice chorus
(defun chorus (sig &optional (depth 0.002)(rate 0.3)(voices 4)(mix 0.5)(limiter 1)
                   &key (phase 0.0))
  (let ((effect (s-rest 1)))
    (dotimes (i voices)
      (setq phase (+ phase (/ (* i 180) voices)))
      (setf vardelay 
        (mult depth 
          (osc (hz-to-step rate) 1 *sine-table* phase)))
      (setf effect
        (sim effect
          (snd-tapv sig depth vardelay (* 2.0 depth)))))
    (setf sig (mult (/ (1+ mix))
      (sum (mult mix effect) sig))))
    (if (= limiter 1)(limit sig) sig))

(if (arrayp s)
  (vector 
    (chorus (aref s 0) depth rate voices mix limiter :phase 0)
    (chorus (aref s 1) depth rate voices mix limiter :phase 180))
  (chorus s depth rate voices mix limiter))