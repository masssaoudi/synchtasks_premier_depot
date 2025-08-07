<template>
  <div class="pa-inscription-container">
    <div class="inscription-card">
      <h2>👥 Inscription Personne Aidante</h2>
      <p class="subtitle">
        Créez votre compte pour accompagner des utilisateurs
      </p>

      <form class="inscription-form" @submit.prevent="registerPA">
        <div class="form-group">
          <label for="username">Nom d'utilisateur *</label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="Votre nom d'utilisateur"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="email">Email *</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="votre@email.com"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="fullName">Nom complet *</label>
          <input
            id="fullName"
            v-model="form.full_name"
            type="text"
            placeholder="Votre nom complet"
            required
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="phone">Téléphone</label>
          <input
            id="phone"
            v-model="form.phone"
            type="tel"
            placeholder="0123456789"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="password">Mot de passe *</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="Votre mot de passe"
            required
            minlength="6"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label for="confirmPassword">Confirmer le mot de passe *</label>
          <input
            id="confirmPassword"
            v-model="confirmPassword"
            type="password"
            placeholder="Confirmez votre mot de passe"
            required
            class="form-input"
          />
        </div>

        <div class="form-actions">
          <button
            type="submit"
            :disabled="loading || !isFormValid"
            class="btn btn-primary btn-large"
          >
            <span v-if="loading">⏳ Création en cours...</span>
            <span v-else>✅ Créer mon compte PA</span>
          </button>
        </div>
      </form>

      <div v-if="message" :class="['message', messageType]">
        {{ message }}
      </div>

      <div class="login-link">
        <p>
          Déjà inscrit ? <router-link to="/pa-login">Se connecter</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';

  export default {
    name: 'PAInscriptionView',
    setup() {
      const router = useRouter();
      const loading = ref(false);
      const message = ref('');
      const messageType = ref('');
      const confirmPassword = ref('');

      const form = ref({
        username: '',
        email: '',
        full_name: '',
        phone: '',
        password: '',
      });

      const isFormValid = computed(() => {
        return (
          form.value.username &&
          form.value.email &&
          form.value.full_name &&
          form.value.password &&
          form.value.password === confirmPassword.value &&
          form.value.password.length >= 6
        );
      });

      const registerPA = async () => {
        if (!isFormValid.value) {
          message.value =
            'Veuillez remplir tous les champs obligatoires et confirmer votre mot de passe';
          messageType.value = 'error';
          return;
        }

        loading.value = true;
        message.value = '';

        try {
          const response = await fetch(
            'http://localhost:8000/api/auth/register-pa',
            {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify(form.value),
            }
          );

          const data = await response.json();

          if (response.ok && data.success) {
            message.value =
              'Compte créé avec succès ! Vous pouvez maintenant vous connecter.';
            messageType.value = 'success';

            // Rediriger vers la page de connexion PA après 2 secondes
            setTimeout(() => {
              router.push('/pa-login');
            }, 2000);
          } else {
            message.value =
              data.message || 'Erreur lors de la création du compte';
            messageType.value = 'error';
          }
        } catch (error) {
          console.error('Erreur:', error);
          message.value = 'Erreur de connexion au serveur';
          messageType.value = 'error';
        } finally {
          loading.value = false;
        }
      };

      return {
        form,
        confirmPassword,
        loading,
        message,
        messageType,
        isFormValid,
        registerPA,
      };
    },
  };
</script>

<style scoped>
  .pa-inscription-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
  }

  .inscription-card {
    background: white;
    border-radius: 16px;
    padding: 40px;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 500px;
  }

  .inscription-card h2 {
    text-align: center;
    color: #333;
    margin-bottom: 8px;
    font-size: 28px;
  }

  .subtitle {
    text-align: center;
    color: #666;
    margin-bottom: 32px;
    font-size: 16px;
  }

  .inscription-form {
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .form-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .form-group label {
    font-weight: 600;
    color: #333;
    font-size: 14px;
  }

  .form-input {
    padding: 12px 16px;
    border: 2px solid #e1e5e9;
    border-radius: 8px;
    font-size: 16px;
    transition: border-color 0.3s ease;
  }

  .form-input:focus {
    outline: none;
    border-color: #667eea;
  }

  .form-actions {
    margin-top: 24px;
  }

  .btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
  }

  .btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
  }

  .btn-primary:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  }

  .btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  .btn-large {
    padding: 16px 24px;
    font-size: 18px;
  }

  .message {
    margin-top: 20px;
    padding: 12px 16px;
    border-radius: 8px;
    text-align: center;
    font-weight: 500;
  }

  .message.success {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }

  .message.error {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }

  .login-link {
    margin-top: 24px;
    text-align: center;
  }

  .login-link a {
    color: #667eea;
    text-decoration: none;
    font-weight: 600;
  }

  .login-link a:hover {
    text-decoration: underline;
  }

  @media (max-width: 600px) {
    .inscription-card {
      padding: 24px;
      margin: 10px;
    }

    .inscription-card h2 {
      font-size: 24px;
    }
  }
</style>
