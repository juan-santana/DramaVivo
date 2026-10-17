import { ref } from 'vue'

export interface ToastMessage {
  id: string
  title?: string
  message: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
}

const toasts = ref<ToastMessage[]>([])

export function useToast() {
  function show(message: string, type: ToastMessage['type'] = 'info', title?: string, duration = 4000) {
    const id = `toast-${Date.now()}-${Math.random().toString(36).substring(2, 7)}`
    const toast: ToastMessage = {
      id,
      title,
      message,
      type,
      duration,
    }
    toasts.value.push(toast)

    if (duration > 0) {
      setTimeout(() => {
        dismiss(id)
      }, duration)
    }

    return id
  }

  function success(message: string, title = 'Éxito') {
    return show(message, 'success', title)
  }

  function error(message: string, title = 'Error') {
    return show(message, 'error', title, 5000)
  }

  function warning(message: string, title = 'Atención') {
    return show(message, 'warning', title)
  }

  function info(message: string, title = 'Información') {
    return show(message, 'info', title)
  }

  function dismiss(id: string) {
    toasts.value = toasts.value.filter(t => t.id !== id)
  }

  return {
    toasts,
    show,
    success,
    error,
    warning,
    info,
    dismiss,
  }
}
